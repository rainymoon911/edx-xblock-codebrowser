introduction
======

it is a xblock for codebrowser(woboq) and the code is on gitlab

the python code is just a UI(standard xblock) and the kern code is in xblock-script


function of scripts
======

create.sh :               run on gitlab server,called by exp file

initialize_user.sh :      generate the ssh key(private and public),call the initialize.exp to initialize gitlab 
account,upload the project and write gitlab config file(switch users)

initialize_user.exp :     log in gitlab server(root) , use the gitlab cli to create user,upload pub key,and create a empty 
project

generator.sh :            pull code from gitlab, generate the compile commands(in json format),adn generate the html file for browsing code


preparation
======
step 1 

install gitlab

I just use this
[gitlab image on turkey](http://www.turnkeylinux.org/gitlab)

step 2

install cli and configuration

    gem install gitlab
    
    vi .profile
    
    export GITLAB_API_ENDPOINT='http://example.net/api/v3'
    export GITLAB_API_PRIVATE_TOKEN='your private token in admin account'
    
run the command "gitlab" and you can see the help if all right

the gitlab cli dont't provide a function to upload ssh key to a specified user ,so i add a function

    vi /var/lib/gems/1.9.1/gems/gitlab-3.3.0/lib/gitlab/client/users.rb(if you don't use the image,change the dir)
    
add the function create_user_ssh_key

    # Creates a new SSH key to a specified user. Only available to admin users.

    # @example
    #   Gielab.create_user_ssh_key('id','key title','key body')
    #
    # @param  [Integer] id- The ID of a user
    # @param  [String]  title- New SSH key's title
    # @param  [String]  key- New SSH Key
    # @return [Gitlab::ObjectifiedHash] Information about created SSH key.
    def create_user_ssh_key(id, title, key)
      post("/users/#{id}/keys", :body => {:title => title, :key => key})
    end
    
the gitlab API dir is /home/git/gitlab/lib/api

step 3 

create no-password ssh connect between edx server and gitlab server(make exp file easy and safe)

in edx server,generate ssh key and move pub key to gitlab server
    
    ssh-keygen -b 1024 -t rsa
    
    scp .ssh/id_dsa.pub remote_usrname@gitlab server ip:
    
    ssh-add id_rsa
    
if ssh agent haven't start,add the command to .bashrc or .profile to start ssh-agent when user log in

    eval `ssh-agent -s`
    
    
log in gitlab server
    
    mkdir ~/.ssh(if the home dir don't have .ssh)
    
    chmod 700 ~/.ssh
    
    mv id_rsa.pub ~/.ssh
    
    cd ~/.ssh
    
    cat id_rsa.pub >> authorized_keys2
    
    rm -f id_rsa.pub
    
    chmod 600 authorized_keys2
    
now you can log in the gitlab server without password:
    
    ssh root@ip

install woboq codebrowser 
======

[woboq project on github](https://github.com/woboq/woboq_codebrowser/)

modify the args in scripts and other files to suit your project

    
    
    
    



