======
introduction

it is a xblock for codebrowser(woboq) and the code is on gitlab

the python code is just a UI(standard xblock) and the kern code is in xblock-script

======
function of scripts

create.sh               run on gitlab server,called by exp file

initialize_user.sh      generate the ssh key(private and public),call the initialize.exp to initialize gitlab 
account,upload the project and write gitlab config file(switch users)

initialize_user.exp     log in gitlab server(root) , use the gitlab cli to create user,upload pub key,and create a empty 
project

generator.sh            pull code from gitlab, generate the compile commands(in json format),adn generate the html file
for browsing code

======
preparation

