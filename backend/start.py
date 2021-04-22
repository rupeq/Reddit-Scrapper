import os


def execute_command(commands):
    for command in commands:
        os.system(command)


def make_choice():
    postgres = ['p', 'P', 'р']
    mongo = ['m', 'M', 'м']

    mongo_commands = ['docker-compose -f docker-compose-mongo.yml build',
                      'docker-compose -f docker-compose-mongo.yml up']

    postgres_commands = ['docker-compose -f docker-compose-postgres.yml build',
                         'docker-compose -f docker-compose-postgres.yml up']

    while True:
        choice = input("Write p to work with postgres. \nWrite m to work with mongo. \n")

        if choice in postgres:
            execute_command(postgres_commands)
            break
        elif choice in mongo:
            execute_command(mongo_commands)
            break


if __name__ == "__main__":
    make_choice()
