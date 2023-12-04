from itertools import count
import database
import datetime
from Sheet import Sheet
import os
from backend import pathStructure, binary_model_funcs, localization_model_funcs
import texts
import inspect


class dataBaseUtils:
    def __init__(self, ui_obj, user_name="root", password="root"):
        self.db = database.dataBase(
            user_name, password, "localhost", "saba_database", logger_obj=ui_obj.logger
        )
        self.sheets_info_tabel = "sheets_info"
        self.setting_tabel = "settings"
        self.datasets_table = "datasets"
        self.camera_settings_table = "camera_settings"
        self.defects_table = "defects_info"
        self.sign_tables = "sign_tables"
        self.table_user = "users"
        self.table_cameras = "camera_settings"
        self.image_processing = "image_processing"
        self.dataset = "datasets "
        self.plc = "plc_path"
        self.ui_obj = ui_obj
        self.piplines_evaluation_info='piplines_info'
        self.piplines='piplines'
    def check_table_exist(self, table_name):
        ret = self.db.check_table_exist(table_name)
        return ret

    def check_connection(self):
        ret = self.db.check_connection()
        return ret
        # ________________________________________________________________

    #
    # ________________________________________________________________
    def build_sheet(self, record):
        y, m, d = record["date"].split("/")
        hh, mm, _ = record["time"].split(":")
        sheet_obj = Sheet(
            id=record["id"],
            sheet_id=record["sheet_id"],
            main_path=record["main_path"],
            image_format=record["image_format"],
            heat_number=record["heat_number"],
            ps_number=record["ps_number"],
            pdl_number=record["pdl_number"],
            width=record["width"],
            lenght=record["lenght"],
            thickness=record["thickness"],
            date=datetime.date(int(y), int(m), int(d)),
            time=datetime.time(int(hh), int(mm)),
            user=record["user"],
            nframe=record["nframe"],
            cameras=[
                int(record["cameras"].split("-")[0]),
                int(record["cameras"].split("-")[1]),
            ],
        )
        return sheet_obj

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def set_sheet(self, coil_dict):
        data = ()
        db_headers = ""
        for key in coil_dict:
            data = data + (coil_dict[key],)
            db_headers = db_headers + key + ","
        db_headers = "(" + db_headers[:-1] + ")"
        # print('bmodel_record:', data, 'cols:', db_headers)
        try:
            res = self.db.add_record(
                data,
                table_name=self.sheets_info_tabel,
                parametrs=db_headers,
                len_parameters=len(coil_dict),
            )
            return "True"

        except:
            return "Databas Eror"

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def load_sheet(self, id):
        res, record = self.db.search(self.sheets_info_tabel, "sheet_id", id)
        record = record[0]

        return self.build_sheet(record)

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def load_sheets(self, ids):
        sheets = []
        for id in ids:
            res, record = self.db.search(self.sheets_info_tabel, "sheet_id", id)
            record = record[0]

            sheets.append(self.build_sheet(record))
        return sheets

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def get_camera_setting(self):
        x = self.db.report_last(self.camera_settings_table, "id", "0")

        # cam_setting = self.db.search( 'camera_settings', 'id', id )[0]

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def report_last_sheets(self, count):

        records = self.db.report_last(self.sheets_info_tabel, "sheet_id", count)
        res = []
        for record in records:
            res.append(self.build_sheet(record))
        return res

    # ________________________________________________________________
    #
    # ________________________________________________________________
    def set_dataset_path(self, path):
        #  update_record(self,data,table_name,col_name,value,id,id_value):
        self.db.update_record(
            table_name=self.setting_tabel,
            col_name="path_dataset",
            value=path,
            id="id",
            id_value=0,
        )

    def get_dataset(self, value=0):
        res, record = self.db.search(
            table_name=self.datasets_table, param_name="id", value=value
        )
        record = record[0]
        return record

    def get_parent_path(self, value=0):
        res, record = self.db.search(
            table_name=self.setting_tabel, param_name="id", value=value
        )
        record = record[0]
        return record["parent_path"]

    def set_dataset_path_user(self, path):
        #  update_record(self,data,table_name,col_name,value,id,id_value):
        self.db.update_record(
            table_name=self.setting_tabel,
            col_name="path_dataset_user",
            value=path,
            id="id",
            id_value=0,
        )

    # def set_split_size(self, size, id):
    #     self.db.update_record(table_name=self.datasets_table, col_name='split_size', value=str(size), id='id', id_value=id)
    #
    # def get_split_size(self, id):
    #     record =self.db.search(table_name=self.datasets_table,param_name='id',value=id)[0 ]
    #     return eval(record['split_size'])

    def get_path_sheet_image(self, filtered_selected):
        paths = []
        for sheet_id, side, (ncam, nframe) in filtered_selected:
            sheet = self.load_sheet(sheet_id)
            path = pathStructure.sheet_image_path(
                sheet.get_main_path(),
                sheet_id,
                side,
                ncam,
                nframe,
                sheet.get_image_format(),
            )

            paths.append(path)

        return paths

    def get_image_processing_params(self):
        res, img_proc_info = self.db.get_all_content(self.image_processing)
        img_proc_info = img_proc_info[0]
        return list(img_proc_info.values())[1:]

    def get_defects(self):

        res, defects_info = self.db.get_all_content(self.defects_table)

        name_list = []
        for i in range(len(defects_info)):
            name_list.append(defects_info[i]["name"])

        return name_list, defects_info

    def get_defect_id(self, selected_label):
        try:
            res, record = self.db.search(
                self.defects_table, "name", selected_label, int_type=False
            )
            record = record[0]
            return record["defect_ID"]
        except:
            return []

    def search_defect_by_id(self, input_defect_id):
        """this function is used to search a defect in database using its id

        :param input_defect_id: defect id
        :type input_defect_id: str
        :return: defect info
        :rtype: dict
        """

        try:
            res, record = self.db.search("defects_info", "defect_ID", input_defect_id)
            record = record[0]
            # print('asd',record)
            return record
        except:
            return []

    def ret_sign_defect_table(self):

        res, sign = self.db.search(self.sign_tables, "id", "0")

        return sign[0]["defects_info"]

    def update_sign_table(self, col_name, value, id="id", id_value=0):

        self.db.update_record(self.sign_tables, col_name, value, id, id_value)

    def load_cam_params(self, input_camera_id):

        try:
            res, record = self.db.search(self.table_cameras, "id", input_camera_id)
            record = record[0]
            # print('camera info:', record)
            # print('recor',record)
            return record
        except:
            return []

    # _____________________________________________________________________________________
    # binary-models

    def get_binary_models(
        self,
        count=False,
        limit=False,
        limit_size=20,
        offset=0,
        type_model="binary_models",
    ):
        """this function is used to get binary models infoes list from database

        :param count: a boolean determining whether to get count of table, defaults to False, defaults to False
        :type count: bool, optional
        :param limit: boolean to get table records by limit size, defaults to False
        :type limit: bool, optional
        :param limit_size: number of returning rows from database, defaults to 20
        :type limit_size: int, optional
        :param offset: start row index in table to return next n rows, defaults to 0
        :type offset: int, optional
        :return: list of binary model info (in dict)
        :rtype: list of dicts
        """

        res, bmodels = self.db.get_all_content(
            type_model,
            count=count,
            limit=limit,
            limit_size=limit_size,
            offset=offset,
            reverse_order=True,
        )

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_bmodels"]["en"], level=1
            )
            return True, bmodels

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_bmodels_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, bmodels

    #____________________________________________JJ ZONE
    def get_piplines_history_form_db(
        self,
        count=False,
        limit=False,
        limit_size=20,
        offset=0,
    ):


        res, history = self.db.get_all_content(
            'piplins_info',
            count=count,
            limit=limit,
            limit_size=limit_size,
            offset=offset,
            reverse_order=True,
        )
        print('zdknvnkljn--------------------------------------------------------------->',res)
        print('zdknvnkljn--------------------------------------------------------------->',history)
        # validation
        if res == database.SUCCESSFULL:
            # self.ui_obj.logger.create_new_log(
            #     message=texts.MESSEGES["database_get_bmodels"]["en"], level=1
            # )
            return True, history

        #elif res == database.CONNECTION_ERROR:
        #     self.ui_obj.logger.create_new_log(
        #         message=texts.ERRORS["database_conection_failed"]["en"], level=4
        #     )
        # # exception error
        # else:
        #     self.ui_obj.logger.create_new_log(
        #         message=texts.ERRORS["database_get_bmodels_failed"]["en"], level=4
        #     )
        #     self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, history
    #____________________________________________JJ ZONE
    
    def add_binary_model_record(self, params):
        """this function is used to add new binary model parameters to database

        :param params: model parameters (col values)
        :type params: _type_
        :return: _description_
        :rtype: _type_
        """

        data = ()
        db_headers = ""
        for db_header in binary_model_funcs.binary_headers_db:
            data = data + (params[db_header],)
            db_headers = db_headers + db_header + ","
        db_headers = "(" + db_headers[:-1] + ")"

        res = self.db.add_record(
            data,
            table_name="binary_models",
            parametrs=db_headers,
            len_parameters=len(binary_model_funcs.binary_headers_db),
        )

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_add_bmodel"]["en"], level=1
            )
            return True

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_add_bmodel_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False


    def search_binary_model_by_filter(
        self,
        parms,
        cols,
        limit=False,
        limit_size=20,
        offset=0,
        count=False,
        model_type="binary_models",
    ):
        """this function is used to search in binary models table by filtering params

        :param parms: filtering parameters
        :type parms: list
        :param cols: coloumn names to filter
        :type cols: list
        :param limit: boolean to determine returning a part of table rows, defaults to False
        :type limit: bool, optional
        :param limit_size: n returning rows (records), defaults to 20
        :type limit_size: int, optional
        :param offset: starting index to return n next rows, defaults to 0
        :type offset: int, optional
        :param count: boolean determining whether to get count of table, defaults to False
        :type count: bool, optional
        :return:
            result: boolean to determine result
            table_content: list of dicts containing table records, if count==True: count of table
        :rtype: _type_
        """

        res, record = self.db.search_with_range(
            model_type,
            cols,
            parms,
            limit=limit,
            limit_size=limit_size,
            offset=offset,
            count=count,
        )
        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_bmodels"]["en"], level=1
            )
            return True, record

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_bmodels_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, record

    # ________________________________________________________________________________________________________
    # localization models
    def get_localization_models(self, count=False, limit=False, limit_size=20, offset=0):
        """this function is used to get localization models info list from database

        :param count: a boolean determining whether to get count of table, defaults to False, defaults to False
        :type count: bool, optional
        :param limit: boolean to get table records by limit size, defaults to False
        :type limit: bool, optional
        :param limit_size: number of returning rows from database, defaults to 20
        :type limit_size: int, optional
        :param offset: start row index in table to return next n rows, defaults to 0
        :type offset: int, optional
        :return: list of localization model info (in dict)
        :rtype: list of dicts
        """
        
        res, lmodels = self.db.get_all_content('localization_models', count=count, limit=limit, limit_size=limit_size, offset=offset, reverse_order=True)

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(message=texts.MESSEGES['database_get_lmodels']['en'], level=1)
            return True, lmodels
        
        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(message=texts.ERRORS['database_conection_failed']['en'], level=4)
        # exception error
        else:
            self.ui_obj.logger.create_new_log(message=texts.ERRORS['database_get_lmodels_failed']['en'], level=4)
            self.ui_obj.logger.create_new_log(message=res, level=4)
        
        return False, lmodels
    
    def add_localization_model_record(self, params):
        """this function is used to add new localization model parameters to database

        :param params: model parameters (col values)
        :type params: _type_
        :return: _description_
        :rtype: _type_
        """

        data = ()
        db_headers = ""
        for db_header in localization_model_funcs.localization_headers_db:
            data = data + (params[db_header],)
            db_headers = db_headers + db_header + ","
        db_headers = "(" + db_headers[:-1] + ")"

        res = self.db.add_record(
            data,
            table_name="localization_models",
            parametrs=db_headers,
            len_parameters=len(localization_model_funcs.localization_headers_db),
        )

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_add_lmodel"]["en"], level=1
            )
            return True

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_add_lmodel_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False
   
    def search_localization_model_by_filter(self, parms, cols, limit=False, limit_size=20, offset=0, count=False):
        """this function is used to search in localization models table by filtering params

        :param parms: filtering parameters
        :type parms: list
        :param cols: coloumn names to filter
        :type cols: list
        :param limit: boolean to determine returning a part of table rows, defaults to False
        :type limit: bool, optional
        :param limit_size: n returning rows (records), defaults to 20
        :type limit_size: int, optional
        :param offset: starting index to return n next rows, defaults to 0
        :type offset: int, optional
        :param count: boolean determining whether to get count of table, defaults to False
        :type count: bool, optional
        :return:
            result: boolean to determine result
            table_content: list of dicts containing table records, if count==True: count of table
        :rtype: _type_
        """

        res, record = self.db.search_with_range('localization_models', cols, parms, limit=limit, limit_size=limit_size, offset=offset, count=count)
        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(message=texts.MESSEGES['database_get_lmodels']['en'], level=1)
            return True, record

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(message=texts.ERRORS['database_get_lmodels_failed']['en'], level=4)
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, record

    # ________________________________________________________________________________________________________
    # classification models
    def get_cls_models(self, count=False, limit=False, limit_size=20, offset=0):
        """this function is used to get classification models from database

        :param count: boolean determiniing whether to get count of table, defaults to False
        :type count: bool, optional
        :param limit: boolean determining whether to get part of the table, defaults to False
        :type limit: bool, optional
        :param limit_size: parameter to get n rows of table, defaults to 20
        :type limit_size: int, optional
        :param offset: startting irow index to get n next rowa, defaults to 0
        :type offset: int, optional
        :return: _description_
        :rtype: _type_
        """

        res, bmodels = self.db.get_all_content(
            "classification_models",
            count=count,
            limit=limit,
            limit_size=limit_size,
            offset=offset,
            reverse_order=True,
        )

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_classmodels"]["en"], level=1
            )
            return True, bmodels

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_classmodels_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, bmodels

    #
    def search_cls_model_by_filter(
        self, parms, cols, limit=False, limit_size=20, offset=0, count=False
    ):
        """this function is used to search/filter classification models recrds in database

        :param parms: value of filtering cols
        :type parms: list of str
        :param cols: name of cols to filter
        :type cols: list of str
        :param limit: boolean determinin gwhther to get part of records, defaults to False
        :type limit: bool, optional
        :param limit_size: determininng num records to return, defaults to 20
        :type limit_size: int, optional
        :param offset: sarting row index to get n next rows, defaults to 0
        :type offset: int, optional
        :param count: boolean determining count of filtered records, defaults to False
        :type count: bool, optional
        :return: _description_
        :rtype: _type_
        """

        res, record = self.db.search_with_range_with_classes(
            "classification_models",
            cols,
            parms,
            limit=limit,
            limit_size=limit_size,
            offset=offset,
            count=count,
        )

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_filtered_cls_models"]["en"],
                level=1,
            )
            return True, record

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_filtered_cls_models_failed"]["en"],
                level=4,
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, record

    # ______________________________________________________________________________________
    # defects
    def load_defects(self):
        """this function is used to get all defects info from table"""

        res, defects = self.db.get_all_content("defects_info")

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_defects"]["en"], level=1
            )
            return True, defects

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_defects_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, defects

    def search_defect_group_by_id(self, input_defect_group_id):
        """this function is used to search a defect group by its id on database

        :param input_defect_group_id: defect group id
        :type input_defect_group_id: str
        :return: defect group info
        :rtype: str
        """

        res, record = self.db.search(
            "defect_groups", "defect_group_id", input_defect_group_id
        )
        record = record[0]

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_defect_groups"]["en"], level=1
            )
            return True, record

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_defect_groups_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, record

    # ______________________________________________________________________________________________
    # ______________________________________________________________________________________
    # datasets
    def load_datasets(self):
        """this function is used to return datasets from table

        :return: _description_
        :rtype: _type_
        """

        res, datasets = self.db.get_all_content("datasets")

        # validation
        if res == database.SUCCESSFULL:
            self.ui_obj.logger.create_new_log(
                message=texts.MESSEGES["database_get_datasets"]["en"], level=1
            )
            return True, datasets

        elif res == database.CONNECTION_ERROR:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_conection_failed"]["en"], level=4
            )
        # exception error
        else:
            self.ui_obj.logger.create_new_log(
                message=texts.ERRORS["database_get_datasets_failed"]["en"], level=4
            )
            self.ui_obj.logger.create_new_log(message=res, level=4)

        return False, datasets

    # ___________________________________________________________________________________

    # ___________________________________________________________________________________

    def search_user(self, input_user_name):

        try:
            res, record = self.db.search(
                self.table_user, "user_name", input_user_name, int_type=False
            )
            record = record[0]
            res, record_ds = self.db.search(
                self.datasets_table, "id", record["default_dataset"], int_type=False
            )
            record_ds = record_ds[0]
            record["default_dataset"] = record_ds["name"]

            # print('asd',record)
            return record
        except:
            return []

    def get_default_dataset(self, user_name):

        try:
            res, record = self.db.search(
                self.table_user, "user_name", user_name, int_type=False
            )
            record = record[0]

            return record["default_dataset"]
        except:

            return []

    def get_dateset_name(self, id):
        try:
            res, record = self.db.search(self.datasets_table, "id", id, int_type=False)
            record = record[0]

            # print('record',record)

            return record["name"]
        except:
            # print('except')
            return []

    def get_path_dataset(self, dataset_id):

        # try:
        res, record = self.db.search(self.dataset, "id", dataset_id, int_type=False)
        record = record[0]

        # print('record',record)

        return record["path"]
        # except:
        #     print('except')
        #     return []

    def get_all_datasets(self):

        records = self.db.report_last(self.dataset, "id", 99, side="ASC")

        return records

    def get_user_databases(self, user_name, default=True):

        # try:
        res, record = self.db.search(
            self.dataset, "user_own", user_name, int_type=False
        )

        if default:
            res, default_record = self.db.search(self.dataset, "id", 0, int_type=False)
            record += default_record

        default_ds = self.get_default_dataset(user_name)
        # print('*********{}**********'.format(default_ds))

        for i in range(len(record)):
            if str(record[i]["id"]) == default_ds:
                break

        record.insert(0, record.pop(i))

        # print('****record',record)
        return record

    # except:
    #     print('except')
    #     return []

    def update_dataset_default(self, dataset_id, user_name):

        self.db.update_record(
            self.table_user, "default_dataset", str(dataset_id), "user_name", user_name
        )

    def add_dataset(self, data):

        # try:
        res = self.db.add_record(
            data,
            table_name=self.dataset,
            parametrs="(name,user_own,path)",
            len_parameters=3,
        )
        return "True"

        # except:
        #     return 'Databas Eror'

    def set_language_font(self, lang, font):
        self.db.update_record(self.setting_tabel, "language", str(lang), "id", "0")
        self.db.update_record(self.setting_tabel, "font_style", str(font), "id", "0")

    def load_language_font(self):
        res, record = self.db.search(self.setting_tabel, "id", "0")
        record = record[0]
        # print(record)
        return record["language"], record["font_style"]

    def load_plc_parms(self):
        """
        this function is used to load plc params from table

        Args: None

        Returns:
            plc_params: in dict, if failed to load from dataabse, return None
        """
        try:
            res, parms = self.db.get_all_content(self.plc)
            # print(parms)
            return parms

        except:
            return None

    def update_plc_parms(self, plc_parms):
        """
        this function is used to update plc params on database

        Args:
            plc_parms (_type_): in dict

        Returns:
            resault: a boolean determining wheather update is done
        """

        try:
            for _, param in enumerate(plc_parms.keys()):
                # update_record(self,table_name,col_name,value,id,id_value):
                # print('_',_,'   ',param)
                # print(plc_parms[param])

                try:
                    min_value = str(int(plc_parms[param][1]))
                except:
                    min_value = "-1"
                #
                try:
                    max_value = str(int(plc_parms[param][2]))
                except:
                    max_value = "-1"

                res = self.db.update_record(
                    self.plc, "path", str(plc_parms[param][0]), "id", _
                )
                res = self.db.update_record(
                    self.plc, "min_or_off_value", min_value, "id", _
                )
                res = self.db.update_record(
                    self.plc, "max_or_on_value", max_value, "id", _
                )

            return res
        #
        except:
            return False

    def update_plc_ip(self, ip):
        """
        this function is used to update plc ip on table

        Args:
            ip (_type_): plc ip (in string)

        Returns:
            resalt: a boolean determining wheather database updated
        """

        try:
            res = self.db.update_record(self.setting_tabel, "plc_ip", ip, "id", 0)
            return res

        except:
            return False

    def load_plc_ip(self):
        """
        this function is used to load plc ip from table on dataabase

        Returns:
            record: plc ip (in string), if failed return False
        """
        try:
            res, record = self.db.search(self.setting_tabel, "id", 0)
            record = record[0]
            return record["plc_ip"]

        except:
            return False


    def get_pipline_names(self,spec_name=False):
        names=[]
        spec_names=[]
        records = self.db.report_last(self.piplines, "name", 999, side="ASC")
        for name in records:
            names.append(name['name'])
            if spec_name!=False:
                if name['user_own']==spec_name:
                    spec_names.append(name['name'])

        print(names)
        if spec_name==False:
            return names
        
        else:
            return names,spec_names
    



    def add_pipline(self,data):
        try:
            res = self.db.add_record(
                data,
                table_name=self.piplines,
                parametrs="(name,user_own,path,binary_weight_path,localization_weight_path,classification_weight_path)",
                len_parameters=6,
            )
            return True
        except:
            return False



    def remove_pipline(self,name):
        
        res = self.db.remove_record(col_name='name',id=name,table_name=self.piplines)


    # #____________________________________JJ ZONE
    # def update_piplines_info_database(self,record):
    #     y, m, d = record["date"].split("/")
    #     hh, mm, _ = record["time"].split(":")
    #     date=datetime.date(int(y), int(m), int(d))
    #     time=datetime.time(int(hh), int(mm))
        
    #     pipline_name=record['pipline_name']
    #     binary_model=record['binary_model']
    #     localization_model=record['localization_model']
    #     classification_model=record['classification_model']
    #     binary_acc=record['binary_acc']
    #     binary_recall=record['binary_recall']
    #     binary_precision=record['binary_precision']
    #     binary_f1=record['binary_f1']
    #     classification_acc=record['classification_acc']
    #     classification_recall=record['classification_recall']
    #     classification_precision=record['classification_precision']
    #     classification_f1=record['classification_f1']
    #     localization_dice=record['localization_dice']
    #     localization_iou=record['localization_iou']
    #     dataset_name=record['dataset_name']
    #     dataset_path=record['dataset_path']

    # #____________________________________JJ ZONE



if __name__ == "__main__":
    db = dataBaseUtils('Null')
    db.get_pipline_names()
    # x = db.load_plc_parms()
    # # x=db.load_language()
    # print(x)

    # db.set_language("Persian")
    # records = db.load_coil_info(996)
    # db.get_camera_setting()
    # db.set_dataset_path('G:/dataset/')
    # print(db.get_dataset_path())

    # name,defects=db.get_defects()
    # print('name',name)
    # print('defe',defects)

    # x=db.get_sign('defects_info')

    # db.update_sign_table('defects_info','4')
    # d=db.get_user_databases('ali')
    # data=('dataset_name','ali','adwad')
    # d=db.add_dataset(data)
    # print(d)
    # print(x)
    # name,defects=db.get_defects()
    # print('name',name)
    # print('defe',defects)

    # db.get_path(['997', 'up', (5, 5)])
    # pass
