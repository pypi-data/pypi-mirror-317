# import os
from os import path, makedirs

from ...utils.validate_dates import *
from ...utils.validate_hours import validate_hours
from ...utils.get_time_zone import *
from ...utils.numerical_id import *
from ...utils.convert_timestamp import *
from .parse import *
from .MIMS_minute import *
from .MIMS_hour import *
from .MIMS_day import *
from .AUC_minute import *
from .AUC_hour import *
from .AUC_day import *
from .SWaN_minute import *
from .SWaN_hour import *
from .SWaN_day import *
# from .bafToCSV import *
# from .csvToMIMS import *
# from .baf_to_dataframe import *
from .dataframe_to_MIMS import *
from shutil import copyfile
import warnings

# from SWaN_accel import classify

warnings.filterwarnings("ignore")

area = "data-watch"
logs_watch = "logs-watch"
device = "watch"
file_shortname = "accelerometer"

# since the accelerometer file name is mixed with irregular numbers, file name matching is needed.
name_pattern = "AndroidWearWatch"
TASK = "all"
SAMPLING_RATE = 50.0


def reg_exp_matching(hour_folder_path, name_pattern):
    file_list = listdir(hour_folder_path)
    matched_name = ""
    for file_str in file_list:
        if file_str.startswith(name_pattern):
            matched_name = file_str
            break
    return matched_name


def MIMSExist(hour_folder_path):
    # print(str(hour_folder_path))
    exist = False
    path_mims = None
    # in_path = sorted(glob(os.path.join(hour_folder_path, '020000000000-AccelerationCalibrated.*.sensor.csv')))[0]

    # If the MIMS-unit file already exists, import the csv file for concatenation of daily csv
    # tmpDir = os.path.dirname(in_path)
    path_mims_list = glob(os.path.join(hour_folder_path, "mims*.csv"))
    # print('mims path list')
    # print(path_mims_list)

    if len(path_mims_list) > 0:
        path_mims = path_mims_list[0]
        # print(path_mims + " exists. Skipping csv to MIMS conversion for this file.")
        exist = True

    return exist, path_mims


def HARExist(hour_folder_path):
    # print(str(hour_folder_path))
    exist = False
    path_har = None
    path_har_list = glob(os.path.join(hour_folder_path, "har_*.csv"))
    # print('har path list')
    # print(path_har_list)

    if len(path_har_list) > 0:
        path_har = path_har_list[0]
        # print(path_har + " exists. Skipping csv to HAR conversion for this file.")
        exist = True
    return exist, path_har


def pre_process(microT_root_path, intermediate_file_save_path, p_id, date):
    participant_folder_path = microT_root_path
    area_folder_path = participant_folder_path + sep + area
    hours_with_target_file_list = {}  # included in participant stats report
    pid = p_id.split("@timestudy_com")[0]
    numerical_id = getNumericalID(pid)
    if path.exists(area_folder_path):
        date_folder_path = area_folder_path + sep + date
        if path.exists(date_folder_path):
            file_save_date_path = intermediate_file_save_path + sep + "intermediate_file" + sep + p_id + sep + date
            if not path.exists(file_save_date_path):
                makedirs(file_save_date_path)
            day_file_name_mims = device + "_" + file_shortname + "_mims_clean_" + date + ".csv"
            day_file_name_har_intensity = device + "_" + file_shortname + "_har_clean_" + "_intensity_" + date + ".csv"
            day_file_name_har_activity = device + "_" + file_shortname + "_har_clean_" + "_activity_" + date + ".csv"
            day_file_name_har_posture = device + "_" + file_shortname + "_har_clean_" + "_posture_" + date + ".csv"
            day_file_save_path_mims = file_save_date_path + sep + day_file_name_mims
            day_file_save_path_har_intensity = file_save_date_path + sep + day_file_name_har_intensity
            day_file_save_path_har_activity = file_save_date_path + sep + day_file_name_har_activity
            day_file_save_path_har_posture = file_save_date_path + sep + day_file_name_har_posture
            date_swan_file = microT_root_path + sep + area + sep + date + sep + "SWaN_" + date + "_final.csv"
            day_file_name_mims_minute = file_save_date_path + sep + device + "_" + file_shortname + "_mims_minute_" + date + ".csv"
            day_file_name_mims_hour = file_save_date_path + sep + device + "_" + file_shortname + "_mims_hour_" + date + ".csv"
            day_file_name_mims_day = file_save_date_path + sep + device + "_" + file_shortname + "_mims_day_" + date + ".csv"
            p_id_no_domain = p_id.split("@")[0]
            swan_dest = file_save_date_path + sep + device + "_" + file_shortname + "_swan_clean_" + date + ".csv"
            day_file_name_swan_minute = file_save_date_path + sep + device + "_" + file_shortname + "_swan_minute_" + date + ".csv"
            day_file_name_swan_hour = file_save_date_path + sep + device + "_" + file_shortname + "_swan_hour_" + date + ".csv"
            day_file_name_swan_day = file_save_date_path + sep + device + "_" + file_shortname + "_swan_day_" + date + ".csv"

            day_file_name_auc_minute = file_save_date_path + sep + device + "_" + file_shortname + "_auc_minute_" + date + ".csv"
            day_file_name_auc_hour = file_save_date_path + sep + device + "_" + file_shortname + "_auc_hour_" + date + ".csv"
            day_file_name_auc_day = file_save_date_path + sep + device + "_" + file_shortname + "_auc_day_" + date + ".csv"

            # check if swan exists
            if not path.exists(swan_dest):
                if path.exists(date_swan_file):
                    copyfile(date_swan_file, swan_dest)

            if path.exists(swan_dest):
                swan_hour_minute_exist = True
                # swan_hour_minute_exist = False
                if not path.exists(day_file_name_swan_minute) or not path.exists(day_file_name_swan_hour):
                    swan_hour_minute_exist = False
                if not swan_hour_minute_exist:
                    df_swan_date = pd.read_csv(swan_dest)
                    df_swan_minute = get_swan_matrix_minute(df_swan_date)
                    if df_swan_minute is not None:
                        df_swan_minute["PARTICIPANT_ID_TEXT"] = [pid] * len(df_swan_minute)
                        df_swan_minute["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_swan_minute)
                        df_swan_minute = df_swan_minute[
                            ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE",
                             "SWAN_PREDICTION_NUM", "SWAN_PREDICTION"]]
                        df_swan_minute.to_csv(day_file_name_swan_minute, index=False)

                        df_swan_hour = get_swan_matrix_hour(df_swan_minute)
                        df_swan_hour["PARTICIPANT_ID_TEXT"] = [pid] * len(df_swan_hour)
                        df_swan_hour["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_swan_hour)
                        df_swan_hour = df_swan_hour[
                            ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR",
                             "SWAN_PREDICTION_NUM", "WEAR_MINUTES", "NWEAR_MINUTES", "SLEEP_MINUTES",
                             "INDECISIVE_MINUTES"]]
                        df_swan_hour.to_csv(day_file_name_swan_hour, index=False)

                        df_swan_day = get_swan_matrix_day(df_swan_hour)
                        df_swan_day["PARTICIPANT_ID_TEXT"] = [pid] * len(df_swan_day)
                        df_swan_day["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_swan_day)
                        df_swan_day = df_swan_day[
                            ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY",
                             "SWAN_PREDICTION_NUM", "WEAR_MINUTES", "NWEAR_MINUTES", "SLEEP_MINUTES",
                             "INDECISIVE_MINUTES"]]
                        df_swan_day.to_csv(day_file_name_swan_day, index=False)

            mims_dest_exists = True
            # mims_dest_exists = False
            if not path.exists(day_file_save_path_mims):
                mims_dest_exists = False

            har_dest_all_exist = True
            if not path.exists(day_file_save_path_har_activity) or \
                    not path.exists(day_file_save_path_har_intensity) or not path.exists(
                day_file_save_path_har_posture):
                har_dest_all_exist = False

            mims_hour_minute_exist = True
            # mims_hour_minute_exist = False
            if not path.exists(day_file_name_mims_minute) or not path.exists(day_file_name_mims_hour):
                mims_hour_minute_exist = False

            if not mims_dest_exists or not har_dest_all_exist or not mims_hour_minute_exist:
                # if not path.exists(date_swan_file):
                #     print("For date: " + date)
                #     classify.main(sampling_rate=SAMPLING_RATE, input_folder=microT_root_path,
                #                   file_path=p_id_no_domain, startdateStr=date)
                # print(date_swan_file)

                df_participant_mims = pd.DataFrame()
                df_participant_har_intensity = pd.DataFrame()
                df_participant_har_activity = pd.DataFrame()
                df_participant_har_posture = pd.DataFrame()
                date_folder_path = area_folder_path + sep + date
                # check hourly folder
                validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
                if len(validated_hour_list) == 0:
                    print("Cannot find hour folder in {} data".format(date))
                # iterate through hour folders
                hours_with_target_file = len(validated_hour_list)  # included in participant stats report
                for hour in validated_hour_list:
                    hour_folder_path = date_folder_path + sep + hour
                    # time zone
                    time_zone = get_time_zone(hour_folder_path)
                    # step 2.1: read target hourly file, baf to csv, csv to mims
                    target_file_matched = reg_exp_matching(hour_folder_path, name_pattern)
                    # binary_df = None
                    if len(target_file_matched) > 0:
                        target_file_path = hour_folder_path + sep + target_file_matched
                        # compressed_csv_path = bafToCsv(target_file_path) ## Convert this to a data frame first
                        # binary_df = baf_to_dataframe(target_file_path)
                        # if not mims_dest_exists:
                        mimsExist, mims_path = MIMSExist(hour_folder_path)
                        if mims_path is not None:
                            df_hour_mims = pd.read_csv(mims_path)
                            df_hour_mims = parse_raw_df(df_hour_mims, time_zone)
                            df_participant_mims = pd.concat([df_participant_mims, df_hour_mims])

                        if not har_dest_all_exist:
                            # harExists, har_path = HARExist(hour_folder_path)
                            # out_path_general = hour_folder_path + sep + "har_" + date + "_" + hour + ".csv"
                            out_path_intensity = hour_folder_path + sep + "har_" + "intensity" + ".csv"
                            out_path_posture = hour_folder_path + sep + "har_" + "posture" + ".csv"
                            out_path_activity = hour_folder_path + sep + "har_" + "activity" + ".csv"
                            # run_har = True
                            # if not harExists:
                            #     hr_dfs = mhlab.run_har_on_dataframe(TASK, binary_df, SAMPLING_RATE, out_path_general)
                            #     df_hour_activity = hr_dfs['activity']
                            #     df_hour_intensity = hr_dfs['intensity']
                            #     df_hour_posture = hr_dfs['posture']
                            # else:
                            if path.exists(out_path_activity):
                                df_hour_activity = pd.read_csv(out_path_activity)
                                df_participant_har_activity = pd.concat([df_participant_har_activity, df_hour_activity])
                            if path.exists(out_path_intensity):
                                df_hour_intensity = pd.read_csv(out_path_intensity)
                                df_participant_har_intensity = pd.concat(
                                    [df_participant_har_intensity, df_hour_intensity])
                            if path.exists(out_path_posture):
                                df_hour_posture = pd.read_csv(out_path_posture)
                                df_participant_har_posture = pd.concat([df_participant_har_posture, df_hour_posture])

                    else:
                        hours_with_target_file -= 1
                        continue

                    # step 2.2: parse target hourly file
                    # if df_hour_mims.shape[0] != 0:
                    #     df_hour_mims = parse_raw_df(df_hour_mims, time_zone)
                    #     df_participant_mims = pd.concat([df_participant_mims, df_hour_mims])

                    # if df_hour_activity.shape[0] != 0:
                    #     df_participant_har_activity = pd.concat([df_participant_har_activity, df_hour_activity])

                    # if df_hour_intensity.shape[0] != 0:
                    #     df_participant_har_intensity = pd.concat([df_participant_har_intensity, df_hour_intensity])

                    # if df_hour_posture.shape[0] != 0:
                    #     df_participant_har_posture = pd.concat([df_participant_har_posture, df_hour_posture])

                # Add a module for minute-level mims sample number
                df_mims_minute = None
                if df_participant_mims.shape[0] != 0:
                    df_participant_mims.sort_values(by=['LOG_TIME'], ascending=True, inplace=True) # some hourly mims file have extra readings in random order, need to sort to avoid bugs in minute level processing
                    df_participant_mims.reset_index(inplace=True, drop=True)
                    df_mims_minute = get_mims_matrix_minute(df_participant_mims)

                pid = p_id.split("@timestudy_com")[0]
                numerical_id = getNumericalID(pid)

                hours_with_target_file_list[date] = hours_with_target_file
                if df_participant_mims.shape[0] != 0:
                    df_participant_mims["PARTICIPANT_ID_TEXT"] = [pid] * len(df_participant_mims)
                    df_participant_mims["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_participant_mims)
                    df_participant_mims["LOG_TIMESTAMP"] = [convert_readable_time_to_timestamp(x) for x in
                                                            df_participant_mims["LOG_TIME"]]

                    df_participant_mims = df_participant_mims[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "LOG_TIME", "LOG_TIMESTAMP", "MIMS_UNIT"]]

                    df_participant_mims.to_csv(day_file_save_path_mims, index=False)
                if df_participant_har_intensity.shape[0] != 0:
                    df_participant_har_intensity["PARTICIPANT_ID_TEXT"] = [pid] * len(df_participant_har_intensity)
                    df_participant_har_intensity["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(
                        df_participant_har_intensity)
                    df_participant_har_intensity = df_participant_har_intensity[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "START_TIME", "STOP_TIME", "PREDICTION",
                         "SOURCE", "LABELSET"]]
                    df_participant_har_intensity.to_csv(day_file_save_path_har_intensity, index=False)
                if df_participant_har_activity.shape[0] != 0:
                    df_participant_har_activity["PARTICIPANT_ID_TEXT"] = [pid] * len(df_participant_har_activity)
                    df_participant_har_activity["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(
                        df_participant_har_activity)
                    df_participant_har_activity = df_participant_har_activity[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "START_TIME", "STOP_TIME", "PREDICTION",
                         "SOURCE", "LABELSET"]]
                    df_participant_har_activity.to_csv(day_file_save_path_har_activity, index=False)
                if df_participant_har_posture.shape[0] != 0:
                    df_participant_har_posture["PARTICIPANT_ID_TEXT"] = [pid] * len(df_participant_har_posture)
                    df_participant_har_posture["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(
                        df_participant_har_posture)
                    df_participant_har_posture = df_participant_har_posture[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "START_TIME", "STOP_TIME", "PREDICTION",
                         "SOURCE", "LABELSET"]]
                    df_participant_har_posture.to_csv(day_file_save_path_har_posture, index=False)
                if df_mims_minute is not None:
                    df_mims_minute["PARTICIPANT_ID_TEXT"] = [pid] * len(df_mims_minute)
                    df_mims_minute["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_mims_minute)
                    df_mims_minute = df_mims_minute[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE",
                         "MIMS_SAMPLE_NUM", "MIMS_INVALID_SAMPLE_NUM", "MIMS_SUM"]]
                    df_mims_minute.to_csv(day_file_name_mims_minute, index=False)

                    df_mims_hour = get_mims_matrix_hour(df_mims_minute, day_file_name_swan_minute)
                    df_mims_hour["PARTICIPANT_ID_TEXT"] = [pid] * len(df_mims_hour)
                    df_mims_hour["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_mims_hour)
                    df_mims_hour = df_mims_hour[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR",
                         "MIMS_SAMPLE_NUM", "MIMS_INVALID_SAMPLE_NUM", "MIMS_SUM", "MIMS_SAMPLE_NUM_WEAR",
                         "MIMS_SAMPLE_NUM_NONWEAR", "MIMS_SAMPLE_NUM_SLEEP", "MIMS_SUM_WEAR", "MIMS_SUM_NONWEAR",
                         "MIMS_SUM_SLEEP"]]
                    df_mims_hour.to_csv(day_file_name_mims_hour, index=False)

                    df_mims_day = get_mims_matrix_day(df_mims_hour)
                    df_mims_day["PARTICIPANT_ID_TEXT"] = [pid] * len(df_mims_day)
                    df_mims_day["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_mims_day)
                    df_mims_day = df_mims_day[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY",
                         "MIMS_SAMPLE_NUM", "MIMS_INVALID_SAMPLE_NUM", "MIMS_SUM", "MIMS_SAMPLE_NUM_WEAR",
                         "MIMS_SAMPLE_NUM_NONWEAR", "MIMS_SAMPLE_NUM_SLEEP", "MIMS_SUM_WEAR", "MIMS_SUM_NONWEAR",
                         "MIMS_SUM_SLEEP"]]
                    df_mims_day.to_csv(day_file_name_mims_day, index=False)

            # first_second_pass_output/logs-watch
            auc_hour_minute_exists = True
            # auc_hour_minute_exists = False
            if not path.exists(day_file_name_auc_minute) or not path.exists(day_file_name_auc_hour):
                auc_hour_minute_exists = False

            if not auc_hour_minute_exists:
                df_participant_auc = pd.DataFrame()
                date_folder_path = microT_root_path + sep + logs_watch + sep + date
                if not path.exists(date_folder_path):
                    return
                # check hourly folder
                validated_hour_list, HAVE_ALL_HOURS = validate_hours(date_folder_path)
                if len(validated_hour_list) == 0:
                    print("Cannot find hour folder in {}".format(date_folder_path))
                # iterate through hour folders
                for hour in validated_hour_list:
                    hour_folder_path = date_folder_path + sep + hour
                    # time zone
                    # time_zone = get_time_zone(hour_folder_path)
                    # step 2.1: read target hourly file
                    target_file_matched = list(glob(path.join(hour_folder_path, "Watch-AccelSampling*")))
                    # binary_df = None
                    if len(target_file_matched) > 0:
                        target_file_path = target_file_matched[0]
                        try:
                            df_hour_auc = pd.read_csv(target_file_path, header=None, error_bad_lines=False,
                                                      warn_bad_lines=True)
                            df_participant_auc = pd.concat([df_participant_auc, df_hour_auc])
                        except pd.errors.EmptyDataError:
                            # empty file so skip
                            pass
                        except pd.errors.ParserError as pe:
                            print("ParserError---{} {}".format(target_file_path, pe))

                df_participant_auc.reset_index(inplace=True, drop=True)
                df_auc_minute = get_auc_matrix_minute(df_participant_auc)

                if df_auc_minute is not None:
                    df_auc_minute["PARTICIPANT_ID_TEXT"] = [pid] * len(df_auc_minute)
                    df_auc_minute["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_auc_minute)
                    df_auc_minute = df_auc_minute[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE",
                         "SAMPLE_COUNT", "AUC_X", "AUC_Y", "AUC_Z"]]
                    df_auc_minute.to_csv(day_file_name_auc_minute, index=False)

                    df_auc_hour = get_auc_matrix_hour(df_auc_minute)
                    df_auc_hour["PARTICIPANT_ID_TEXT"] = [pid] * len(df_auc_hour)
                    df_auc_hour["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_auc_hour)
                    df_auc_hour = df_auc_hour[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY", "HOUR",
                         "SAMPLE_COUNT", "AUC_X", "AUC_Y", "AUC_Z"]]
                    df_auc_hour.to_csv(day_file_name_auc_hour, index=False)

                    df_auc_day = get_auc_matrix_day(df_auc_hour)
                    df_auc_day["PARTICIPANT_ID_TEXT"] = [pid] * len(df_auc_day)
                    df_auc_day["PARTICIPANT_ID_NUMERIC"] = [numerical_id] * len(df_auc_day)
                    df_auc_day = df_auc_day[
                        ["PARTICIPANT_ID_TEXT", "PARTICIPANT_ID_NUMERIC", "YEAR", "MONTH", "DAY",
                         "SAMPLE_COUNT", "AUC_X", "AUC_Y", "AUC_Z"]]
                    df_auc_day.to_csv(day_file_name_auc_day, index=False)

    return


if __name__ == "__main__":
    microT_root_path = r"E:\data\wocket\Wockets-win32-x64\resources\app\src\srv\MICROT"
    intermediate_file_save_path = r"C:\Users\jixin\Desktop\temp"
    p_id_list = ["aditya4_internal@timestudy_com"]
    date_start = "2020-01-01"
    date_end = "2020-07-01"

    pre_process(microT_root_path, intermediate_file_save_path, p_id_list, date_start)
