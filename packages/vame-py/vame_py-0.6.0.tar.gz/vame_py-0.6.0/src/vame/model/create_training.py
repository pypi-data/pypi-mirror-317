import os
import numpy as np
from pathlib import Path
import scipy.signal
from scipy.stats import iqr
import matplotlib.pyplot as plt
from typing import List, Optional
from vame.logging.logger import VameLogger
from vame.util.auxiliary import read_config
from vame.schemas.states import CreateTrainsetFunctionSchema, save_state
from vame.util.data_manipulation import interpol_all_nans


logger_config = VameLogger(__name__)
logger = logger_config.logger


def plot_check_parameter(
    cfg: dict,
    iqr_val: float,
    num_frames: int,
    X_true: List[np.ndarray],
    X_med: np.ndarray,
) -> None:
    """
    Plot the check parameter - z-scored data and the filtered data.

    Parameters
    ----------
    cfg : dict
        Configuration parameters.
    iqr_val : float
        IQR value.
    num_frames : int
        Number of frames.
    X_true : List[np.ndarray]
        List of true data.
    X_med : np.ndarray
        Filtered data.

    Returns
    -------
    None
        Plot the z-scored data and the filtered data.
    """
    plot_X_orig = np.concatenate(X_true, axis=0).T
    plot_X_med = X_med.copy()
    iqr_cutoff = cfg["iqr_factor"] * iqr_val

    plt.figure()
    plt.plot(plot_X_orig.T)
    plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
    plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
    plt.title("Full Signal z-scored")
    plt.legend()

    if num_frames > 1000:
        rnd = np.random.choice(num_frames)

        plt.figure()
        plt.plot(plot_X_med[:, rnd : rnd + 1000].T)
        plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
        plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
        plt.title("Filtered signal z-scored")
        plt.legend()

        plt.figure()
        plt.plot(plot_X_orig[:, rnd : rnd + 1000].T)
        plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
        plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
        plt.title("Original signal z-scored")
        plt.legend()

        plt.figure()
        plt.plot(plot_X_orig[:, rnd : rnd + 1000].T, "g", alpha=0.5)
        plt.plot(plot_X_med[:, rnd : rnd + 1000].T, "--m", alpha=0.6)
        plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
        plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
        plt.title("Overlayed z-scored")
        plt.legend()

        # plot_X_orig = np.delete(plot_X_orig.T, anchor_1, 1)
        # plot_X_orig = np.delete(plot_X_orig, anchor_2, 1)
        # mse = (np.square(plot_X_orig[rnd:rnd+1000, :] - plot_X_med[:,rnd:rnd+1000].T)).mean(axis=0)

    else:
        plt.figure()
        plt.plot(plot_X_med.T)
        plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
        plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
        plt.title("Filtered signal z-scored")
        plt.legend()

        plt.figure()
        plt.plot(plot_X_orig.T)
        plt.axhline(y=iqr_cutoff, color="r", linestyle="--", label="IQR cutoff")
        plt.axhline(y=-iqr_cutoff, color="r", linestyle="--")
        plt.title("Original signal z-scored")
        plt.legend()

    logger.info(
        "Please run the function with check_parameter=False if you are happy with the results"
    )


def traindata_aligned(
    cfg: dict,
    sessions: List[str],
    testfraction: float,
    savgol_filter: bool,
    check_parameter: bool,
) -> None:
    """
    Create training dataset for aligned data.

    Parameters
    ----------
    cfg : dict
        Configuration parameters.
    sessions : List[str]
        List of sessions.
    testfraction : float
        Fraction of data to use as test data.
    savgol_filter : bool
        Flag indicating whether to apply Savitzky-Golay filter.
    check_parameter : bool
        If True, the function will plot the z-scored data and the filtered data.

    Returns
    -------
    None
        Save numpy arrays with the test/train info to the project folder.
    """
    X_train = []
    pos = []
    pos_temp = 0
    pos.append(0)

    if check_parameter:
        X_true = []
        sessions = [sessions[0]]

    for session in sessions:
        logger.info("z-scoring of session %s" % session)
        path_to_file = os.path.join(
            cfg["project_path"],
            "data",
            "processed",
            session,
            session + "-PE-seq.npy",
        )
        data = np.load(path_to_file)

        X_mean = np.mean(data, axis=None)
        X_std = np.std(data, axis=None)
        X_z = (data.T - X_mean) / X_std

        # Introducing artificial error spikes
        # rang = [1.5, 2, 2.5, 3, 3.5, 3, 3, 2.5, 2, 1.5]
        # for i in range(num_frames):
        #     if i % 300 == 0:
        #         rnd = np.random.choice(12,2)
        #         for j in range(10):
        #             X_z[i+j, rnd[0]] = X_z[i+j, rnd[0]] * rang[j]
        #             X_z[i+j, rnd[1]] = X_z[i+j, rnd[1]] * rang[j]

        if check_parameter:
            X_z_copy = X_z.copy()
            X_true.append(X_z_copy)

        if cfg["robust"]:
            iqr_val = iqr(X_z)
            logger.info(
                "IQR value: %.2f, IQR cutoff: %.2f"
                % (iqr_val, cfg["iqr_factor"] * iqr_val)
            )
            for i in range(X_z.shape[0]):
                for marker in range(X_z.shape[1]):
                    if X_z[i, marker] > cfg["iqr_factor"] * iqr_val:
                        X_z[i, marker] = np.nan

                    elif X_z[i, marker] < -cfg["iqr_factor"] * iqr_val:
                        X_z[i, marker] = np.nan

            X_z = interpol_all_nans(X_z)

        X_len = len(data.T)
        pos_temp += X_len
        pos.append(pos_temp)
        X_train.append(X_z)

    X = np.concatenate(X_train, axis=0)
    # X_std = np.std(X)

    detect_anchors = np.std(X.T, axis=1)
    sort_anchors = np.sort(detect_anchors)
    if sort_anchors[0] == sort_anchors[1]:
        anchors = np.where(detect_anchors == sort_anchors[0])[0]
        anchor_1_temp = anchors[0]
        anchor_2_temp = anchors[1]
    else:
        anchor_1_temp = int(np.where(detect_anchors == sort_anchors[0])[0])
        anchor_2_temp = int(np.where(detect_anchors == sort_anchors[1])[0])

    if anchor_1_temp > anchor_2_temp:
        anchor_1 = anchor_1_temp
        anchor_2 = anchor_2_temp
    else:
        anchor_1 = anchor_2_temp
        anchor_2 = anchor_1_temp

    X = np.delete(X, anchor_1, 1)
    X = np.delete(X, anchor_2, 1)
    X = X.T

    if savgol_filter:
        X_med = scipy.signal.savgol_filter(X, cfg["savgol_length"], cfg["savgol_order"])
    else:
        X_med = X

    num_frames = len(X_med.T)
    test = int(num_frames * testfraction)

    z_test = X_med[:, :test]
    z_train = X_med[:, test:]

    if check_parameter:
        plot_check_parameter(
            cfg=cfg,
            iqr_val=iqr_val,
            num_frames=num_frames,
            X_true=X_true,
            X_med=X_med,
        )
    else:
        # save numpy arrays the the test/train info:
        np.save(
            os.path.join(
                cfg["project_path"],
                "data",
                "train",
                "train_seq.npy",
            ),
            z_train,
        )
        np.save(
            os.path.join(
                cfg["project_path"],
                "data",
                "train",
                "test_seq.npy",
            ),
            z_test,
        )
        for i, session in enumerate(sessions):
            np.save(
                os.path.join(
                    cfg["project_path"],
                    "data",
                    "processed",
                    session,
                    session + "-PE-seq-clean.npy",
                ),
                X_med[:, pos[i] : pos[i + 1]],
            )
        logger.info("Lenght of train data: %d" % len(z_train.T))
        logger.info("Lenght of test data: %d" % len(z_test.T))


def traindata_fixed(
    cfg: dict,
    sessions: List[str],
    testfraction: float,
    num_features: int,
    savgol_filter: bool,
    check_parameter: bool,
    pose_ref_index: Optional[List[int]],
) -> None:
    """
    Create training dataset for fixed data.

    Parameters
    ----------
    cfg : dict
        Configuration parameters.
    sessions : List[str]
        List of sessions.
    testfraction : float
        Fraction of data to use as test data.
    num_features : int
        Number of features.
    savgol_filter : bool
        Flag indicating whether to apply Savitzky-Golay filter.
    check_parameter : bool
        If True, the function will plot the z-scored data and the filtered data.
    pose_ref_index : Optional[List[int]]
        List of reference coordinate indices for alignment.

    Returns:
        None
            Save numpy arrays with the test/train info to the project folder.
    """
    X_train = []
    pos = []
    pos_temp = 0
    pos.append(0)

    if check_parameter:
        X_true = []
        sessions = [sessions[0]]

    for session in sessions:
        logger.info("z-scoring of file %s" % session)
        path_to_file = os.path.join(
            cfg["project_path"],
            "data",
            "processed",
            session,
            session + "-PE-seq.npy",
        )
        data = np.load(path_to_file)

        X_mean = np.mean(data, axis=None)
        X_std = np.std(data, axis=None)
        X_z = (data.T - X_mean) / X_std

        if check_parameter:
            X_z_copy = X_z.copy()
            X_true.append(X_z_copy)

        if cfg["robust"]:
            iqr_val = iqr(X_z)
            logger.info(
                "IQR value: %.2f, IQR cutoff: %.2f"
                % (iqr_val, cfg["iqr_factor"] * iqr_val)
            )
            for i in range(X_z.shape[0]):
                for marker in range(X_z.shape[1]):
                    if X_z[i, marker] > cfg["iqr_factor"] * iqr_val:
                        X_z[i, marker] = np.nan

                    elif X_z[i, marker] < -cfg["iqr_factor"] * iqr_val:
                        X_z[i, marker] = np.nan

                X_z[i, :] = interpol_all_nans(X_z[i, :])

        X_len = len(data.T)
        pos_temp += X_len
        pos.append(pos_temp)
        X_train.append(X_z)

    X = np.concatenate(X_train, axis=0).T

    if savgol_filter:
        X_med = scipy.signal.savgol_filter(X, cfg["savgol_length"], cfg["savgol_order"])
    else:
        X_med = X

    num_frames = len(X_med.T)
    test = int(num_frames * testfraction)

    z_test = X_med[:, :test]
    z_train = X_med[:, test:]

    if check_parameter:
        plot_check_parameter(
            cfg,
            iqr_val,
            num_frames,
            X_true,
            X_med,
        )

    else:
        if pose_ref_index is None:
            raise ValueError(
                "Please provide a pose reference index for training on fixed data. E.g. [0,5]"
            )
        # save numpy arrays the the test/train info:
        np.save(
            os.path.join(
                cfg["project_path"],
                "data",
                "train",
                "train_seq.npy",
            ),
            z_train,
        )
        np.save(
            os.path.join(
                cfg["project_path"],
                "data",
                "train",
                "test_seq.npy",
            ),
            z_test,
        )

        y_shifted_indices = np.arange(0, num_features, 2)
        x_shifted_indices = np.arange(1, num_features, 2)
        belly_Y_ind = pose_ref_index[0] * 2
        belly_X_ind = (pose_ref_index[0] * 2) + 1

        for i, session in enumerate(sessions):
            # Shifting section added 2/29/2024 PN
            X_med_shifted_file = X_med[:, pos[i] : pos[i + 1]]
            belly_Y_shift = X_med[belly_Y_ind, pos[i] : pos[i + 1]]
            belly_X_shift = X_med[belly_X_ind, pos[i] : pos[i + 1]]

            X_med_shifted_file[y_shifted_indices, :] -= belly_Y_shift
            X_med_shifted_file[x_shifted_indices, :] -= belly_X_shift

            np.save(
                os.path.join(
                    cfg["project_path"],
                    "data",
                    "processed",
                    session,
                    session + "-PE-seq-clean.npy",
                ),
                X_med_shifted_file,
            )  # saving new shifted file

        logger.info("Lenght of train data: %d" % len(z_train.T))
        logger.info("Lenght of test data: %d" % len(z_test.T))


@save_state(model=CreateTrainsetFunctionSchema)
def create_trainset(
    config: str,
    pose_ref_index: Optional[List] = None,
    check_parameter: bool = False,
    save_logs: bool = False,
) -> None:
    """
    Creates a training and test datasets for the VAME model.
    Fills in the values in the "create_trainset" key of the states.json file.
    Creates the training dataset for VAME at:
    - project_name/
        - data/
            - session00/
                - session00-PE-seq-clean.npy
            - session01/
                - session01-PE-seq-clean.npy
            - train/
                - test_seq.npy
                - train_seq.npy

    The produced -clean.npy files contain the aligned time series data in the
    shape of (num_dlc_features - 2, num_video_frames).

    The produced test_seq.npy contains the combined data in the shape of (num_dlc_features - 2, num_video_frames * test_fraction).

    The produced train_seq.npy contains the combined data in the shape of (num_dlc_features - 2, num_video_frames * (1 - test_fraction)).

    Parameters
    ----------
    config : str
        Path to the config file.
    pose_ref_index : Optional[List], optional
        List of reference coordinate indices for alignment. Defaults to None.
    check_parameter : bool, optional
        If True, the function will plot the z-scored data and the filtered data. Defaults to False.
    save_logs : bool, optional
        If True, the function will save logs to the project folder. Defaults to False.

    Returns
    -------
    None
    """
    try:
        config_file = Path(config).resolve()
        cfg = read_config(str(config_file))
        fixed = cfg["egocentric_data"]

        if save_logs:
            log_path = Path(cfg["project_path"]) / "logs" / "create_trainset.log"
            logger_config.add_file_handler(str(log_path))

        if not os.path.exists(os.path.join(cfg["project_path"], "data", "train", "")):
            os.mkdir(os.path.join(cfg["project_path"], "data", "train", ""))

        sessions = []
        if cfg["all_data"] == "No":
            for session in cfg["session_names"]:
                use_session = input("Do you want to train on " + session + "? yes/no: ")
                if use_session == "yes":
                    sessions.append(session)
                if use_session == "no":
                    continue
        else:
            sessions = cfg["session_names"]

        logger.info("Creating training dataset...")
        if cfg["robust"]:
            logger.info(
                "Using robust setting to eliminate outliers! IQR factor: %d"
                % cfg["iqr_factor"]
            )

        if not fixed:
            logger.info(
                "Creating trainset from the vame.egocentrical_alignment() output "
            )
            traindata_aligned(
                cfg,
                sessions,
                cfg["test_fraction"],
                cfg["savgol_filter"],
                check_parameter,
            )
        else:
            logger.info("Creating trainset from the vame.pose_to_numpy() output ")
            traindata_fixed(
                cfg,
                sessions,
                cfg["test_fraction"],
                cfg["num_features"],
                cfg["savgol_filter"],
                check_parameter,
                pose_ref_index,
            )

        if not check_parameter:
            logger.info(
                "A training and test set has been created. Next step: vame.train_model()"
            )

    except Exception as e:
        logger.exception(str(e))
        raise e
    finally:
        logger_config.remove_file_handler()
