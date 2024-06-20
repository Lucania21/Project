import os

class Config:
    def __init__(self, base_path):
        self.base_path = base_path
        self.content_path = os.path.join(base_path, "content/")
        self.summary_path = os.path.join(base_path, "summary/")
        self.quiz_path = os.path.join(base_path, "quiz/")
        self.info_txt_path = os.path.join(base_path, "info/")
        self.create_directories_and_files()

    def create_directories_and_files(self):
        os.makedirs(self.content_path, exist_ok=True)
        os.makedirs(self.summary_path, exist_ok=True)
        os.makedirs(self.quiz_path, exist_ok=True)
        os.makedirs(self.info_txt_path, exist_ok=True)
        
        # Create and initialize info text files
        source_info_path = os.path.join(self.info_txt_path, "source_info.txt")
        sum_info_path = os.path.join(self.info_txt_path, "sum_info.txt")
        quiz_info_path = os.path.join(self.info_txt_path, "quiz_info.txt")

        if not os.path.exists(source_info_path):
            with open(source_info_path, "w") as f:
                f.write("0" + " " * 19)
        if not os.path.exists(sum_info_path):
            with open(sum_info_path, "w") as f:
                f.write("0" + " " * 19)
        if not os.path.exists(quiz_info_path):
            with open(quiz_info_path, "w") as f:
                f.write("0" + " " * 19)

# Initialize global configuration
config = None

def initialize_config(base_path):
    global config
    config = Config(base_path)
    return config