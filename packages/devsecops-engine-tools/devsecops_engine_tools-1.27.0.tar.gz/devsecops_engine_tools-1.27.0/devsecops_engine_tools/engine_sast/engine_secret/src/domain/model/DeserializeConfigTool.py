from devsecops_engine_tools.engine_core.src.domain.model.threshold import Threshold

class DeserializeConfigTool:
    def __init__(self, json_data, tool):
        self.ignore_search_pattern = json_data["IGNORE_SEARCH_PATTERN"]
        self.message_info_engine_secret = json_data["MESSAGE_INFO_ENGINE_SECRET"]
        self.level_compliance = Threshold(json_data['THRESHOLD'])
        self.scope_pipeline = ''
        self.exclude_path = json_data[tool]["EXCLUDE_PATH"]
        self.number_threads = json_data[tool]["NUMBER_THREADS"]
        self.target_branches = json_data["TARGET_BRANCHES"]
        self.enable_custom_rules = json_data[tool]["ENABLE_CUSTOM_RULES"]
        self.external_dir_owner = json_data[tool]["EXTERNAL_DIR_OWNER"]
        self.external_dir_repo = json_data[tool]["EXTERNAL_DIR_REPOSITORY"]
        self.app_id_github = json_data[tool]["APP_ID_GITHUB"]
        self.installation_id_github = json_data[tool]["INSTALLATION_ID_GITHUB"]
        self.tool_version = json_data[tool]["VERSION"]
        self.extradata_rules = json_data[tool]["RULES"]
