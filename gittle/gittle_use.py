import os
from gittle import Gittle
from dulwich.repo import Repo


def GitUpload(file,Name,Email,Password, Repository,Message="Some uploads"):

    origin_uris = Repository
    if not origin_uris.startswith(Name):
        origin_uris = Name+ "/" + origin_uris
    if not origin_uris.startswith("https://github.com/"):
        origin_uris = "https://github.com/" + origin_uris
    if not origin_uris.endswith(".git"):
        origin_uris = origin_uris + ".git"

    path = os.getcwd()

    # Gittle.clone() 会将当前目录下的文件下载到本地，并初始化git工作路径，上传文件正常
    # repo = Gittle.clone("https://github.com/fengfeng0918/gittle.git", path)
    # Gittle.init() 初始化git工作路径，并没有将远程仓库信息拉到本地，上传（push）文件时会将远程库清空
    # repo = Gittle.init(path,origin_uri="https://github.com/fengfeng0918/gittle.git")

    # git init  以下流程正常！！！
    if not os.path.exists(".git"):
        local_repo = Gittle.init(path)
        # local_repo = Gittle.clone(origin_uris,path)
        bares = False   #不会删除远端,重写本地
    else:
        local_repo = Repo(path)
        bares = True  # 不会删除远端,不重写本地

    repo = Gittle(local_repo,origin_uris)
    repo.fetch(bare=bares)

    # Stage file
    if not isinstance(file,list):
        file = [file]
    repo.stage(file)

    # Commiting
    repo.commit(name=Name, email=Email, message=Message,files=file)

    # add remote
    repo.add_remote('origin',origin_uris)

    # Push
    repo.auth(username=Name, password=Password) # Auth for pushing
    repo.push()

# if __name__ == '__main__':
#     file = "requirements.txt"
#     name= "fengfeng0918"
#     email = "527282351@qq.com"
#     password = "*****"
#     Repository = "gittle"
#     GitUpload(file,name, email, password, Repository)
