import yaml
import os

class PromptBuilder:

    def __init__(self, file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, file_name)
        # 获取当前文件所在目录
        with open(yaml_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    # def build(self):
    #
    #     system_prompt = f"""
    #             角色:{ self.config["role"]}
    #             任务:{";".join( self.config["goal"])}
    #             规则:{";".join( self.config["rules"])}
    #             工具:{",".join( self.config["tool"])}
    #             输出格式:{";".join( self.config["output"]["rules"])}
    #     """.strip()
    #     return system_prompt
    def build(self):
        system_prompt = (
            f"角色:{self.config['role']}\n"
            f"任务:{';'.join(self.config['goal'])}\n"
            f"规则:{';'.join(self.config['rules'])}\n"
            f"工具:{','.join(self.config['tool'])}\n"
            f"输出格式:{';'.join(self.config['output']['rules'])}"
        ).strip()
        return system_prompt

if __name__ =="__main__":

    builder = PromptBuilder("email.yaml")
    system_prompt = builder.build()

    print(system_prompt)