import jenkins
from common import read_config


def get_jenkins_allure():
    rc = read_config.ReadConfig()
    jenkins_url = rc.get_inidata("JENKINS", "jenkins_url")
    job_name = rc.get_inidata("JENKINS", "job_name")
    jenkins_username = rc.get_inidata("JENKINS", "jenkins_username")
    jenkins_pw = rc.get_inidata("JENKINS", "jenkins_pw")
    server = jenkins.Jenkins(jenkins_url,username=jenkins_username,password=jenkins_pw)
    job_url = jenkins_url+job_name
    # 获取最后一次构建
    job_last_build_url = server.get_info(job_name)['lastBuild']['url']
    # allure为在jenkins配置的别名
    allure_url = job_last_build_url + "allure"
    return allure_url


if __name__ == '__main__':
    print(get_jenkins_allure())


