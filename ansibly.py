import sys
import os
import requests
from pymongo import MongoClient
import re
import platform


class Generate:
    """

    """
    def __init__(self):
        """

        """
        self.generate()
        self.final_playbook = str()
        system = platform.system()
        if system != 'Windows':
            base_path = os.path.join('etc', 'ansible', 'ansibly')

    def get_vars_data(self):
        """

        :return:
        """
        var = dict()
        try :
            count = int(input("Please enter number of variable definitions [max 10]: "))
        except ValueError as e:
            count = int(input("Please provide Integer value for variable definitions [max 10]: "))
        if type(count) is not int:
            raise ValueError("Integer value expected, but ", type(count), "given!")
        if count > 10:
            self.get_vars_data()
        else:
            for i in range(count):
                var_name = input("Please enter the Variable Name: ")
                var_value = input("Please enter the value for '" + var_name + "': ")
                var[var_name] = var_value
        print(var)
        return var

    def create_roles(self):
        count = int(input("Please enter no. of. roles to be created: [Max 5]"))
        if count > 5:
            self.create_roles()
        else:

            for i in range(1, count + 1):
                name = input("Please enter the name of role {}: ".format(i))
                leaf = ['tasks', 'vars', 'files', 'handlers', 'meta', 'templates']
                try:

                    for j in leaf:
                        dir = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + j))
                        os.makedirs(dir)
                    for k in leaf:
                        if k == 'handlers' or k == 'tasks' or k == 'vars':
                            f = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + k + '/main.yml'))
                            open(f, 'w').close()
                        if k == 'templates':
                            f = os.path.join(os.getcwd() + os.path.join('/etc/ansible/' + name + '/' + k + '/httpd.conf.j2'))
                            open(f, 'w').close()
                except FileExistsError:
                    print("Cannot create the file / directory when that it already exists")

    def generate(self):
        """

        :return:
        """
        decide = input("Do you want to create a simple Playbook or Roles? [P/R]")
        if decide.lower() == 'r':
            self.create_roles()
        else:
            self.final_playbook = '---' + '\n' + '- name: Ansible Playbook' + '\n  hosts: '
            hosts = input("Please enter the host string or IP: ")
            vars_in = input("Do you want to define variables directly into Playbook ? [Y/N]:")
            if vars_in == 'Y' or vars_in == 'y':
                var = self.get_vars_data()
            else:
                var = dict()

            self.final_playbook += hosts + '\n' + '  become: yes' + '\n' + '  become_user: root' + '\n\n' + '  vars:\n'
            if len(var) > 0:
                for key, values in var.items():
                    self.final_playbook += '    ' + key + ': ' + values + '\n'
            self.final_playbook += '\n  tasks:\n'
            user_input = input("Please enter the search keyword for Module:")

            # Database call
            client = MongoClient("mongodb://readonly:readonly@ansibly-shard-00-00-bsfa5.mongodb.net:27017,"
                                 "ansibly-shard-00-01-bsfa5.mongodb.net:27017,ansibly-shard-00-02-bsfa5.mongodb.net:27017/"
                                 "admin?ssl=true&replicaSet=Ansibly-shard-0&authSource=admin&retryWrites=true&w=majority")
            db = client.test
            my_db = client['Module_Index']
            my_collection = my_db.resources
            # user_input = re.compile('/' + user_input + '/')
            # user_input = '/' + user_input + '/'
            # cnt = my_collection.find({"module_name": {'$regex': user_input}}).count()
            result = list()
            for module in my_collection.find({'module_name': {'$regex': user_input}}).distinct('module_name'):
                result.append(module)

            for j in range(1, len(result)):
                print(str(j) + '. ' + result[j-1])

            def excepting():
                row_num = int(input("\nPlease select a module number from above: Ex: 12 :"))
                try:
                    print('\nYou have chosen the Ansible Module "' + str(result[row_num-1]) + '"')
                    # print("Description:", result[row_num - 1][1])
                    return result[row_num - 1]
                except IndexError:
                    print("\nError - Please enter number within the available limit!!! \n")
                    excepting()

            module_name = excepting()

            # Listing the Parameters
            def get_attributes(mod_name):
                info = my_collection.find({"module_name": mod_name})
                # for rec in info:
                #     print(rec)
                # conn = sqlite3.connect("D:\\A\\ansiblator.db")
                # res = conn.execute("SELECT name,parameter,description,req_flag FROM metadata WHERE name = ?", (x,)
                #                    ).fetchall()
                # meta = list()
                # for i in res:
                #     meta.append(i)
                self.final_playbook += '  - name: ' + mod_name + '\n'
                for value in info:
                    self.final_playbook += '    ' + value['Parameter'] + ':'
                    if 'Required Flag' in value:
                        self.final_playbook += '                                    # * Required Field'
                        if 'Type' in value:
                            self.final_playbook += ' & Type = ' + value['Type'] + '\n'
                    else:
                        self.final_playbook += '                                    # Type = ' + value['Type'] + '\n'

                self.final_playbook += '\n'

            get_attributes(module_name)

            decision = input("Do you want to continue: [Y/N]")
            while decision == 'Y' or decision == 'y':
                x = excepting()
                get_attributes(x)
                decision = input("Do you want to continue: [Y/N]")

            self.final_playbook += '\n...'
            print(self.final_playbook + '\n...')
            with open(os.path.join(os.getcwd(),"playbook1.yml"), "w+") as file:
                file.write(self.final_playbook)

