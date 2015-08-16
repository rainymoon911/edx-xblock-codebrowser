import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String
from xblock.fragment import Fragment

import os
import logging.handlers
import pymongo

class CodeBrowserBlock(XBlock):
    """
    An XBlock providing CodeBrowser capabilities for video
    """

    src = String(help="the directory of your code", default=None, scope=Scope.content)
    width = Integer(help="width of the frame", default=800, scope=Scope.content)
    height = Integer(help="height of the frame", default=900, scope=Scope.content)

    def student_view(self, context=None):
        """
        The primary view of the CodeBrowserBlock, shown to students
        when viewing courses.
        """
        student_id = self.runtime.anonymous_student_id

	real_user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
	email = real_user.email
	username = real_user.username


	LOG_FILE = '/var/www/gitlab_codebrowser.log'
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)

        logger = logging.getLogger('gitlab_codebrowser')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

	"""
        save the private key and create cofig file
        """
        rsa_file = '/var/www/.ssh/id_rsa_' + student_id

	
	"""
	pull the code from gitlab and generate the static html files
	"""
	if not os.path.isfile(rsa_file):
		
		try:
		    conn=pymongo.Connection('localhost', 27017)
                    db = conn.test
                    token=db.token
		    result = token.find_one({"username":username})
		    private_key = result["private_key"]
		    logger.info("codebrowser: username" + username)
		    conn.disconnect()
		    #write config file and private key
		    ip　=　”192.168.1.62“
		    port　=　”22“
		    config_file　=　"/var/www/.ssh/config"
		    config　=　"Host " + student_id + "\n HostName " + ip +"\n User git\n Port " + port +"\n IdentityFile " + rsa_file + "\n\n"
		    file_rsa　=　open(rsa_file,'w')
		    file_rsa.write(private_key)
		    file_rsa.close()
		    file_config　=　open(config_file,'wa')
		    file_config.write(config)
		    file_config.close()
		    os.system("chmod 600 ” + rsa_file)
		    #create code dir
		    dir = "/edx/var/edxapp/staticfiles/ucore/" + student_id + "/ucore_lab"
		    os.system("mkdir -p " + dir +  " && cd " + dir + " && git init")

		except Exception, ex:
		    logger.info("Error in codebrowser(get private key)" + username + ex)
                    #return self.message_view("Error in codebrowser (get private key,please make sure you have git account)", ex, context)
	
	
        
	# Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__, "static/html/codebrowser_view.html")
	
        frag = Fragment(unicode(html_str).format(
		width=self.width, 
		height=self.height,
		student_id=student_id,
		email=email,
	))
        # Load CSS
        css_str = pkg_resources.resource_string(__name__, "static/css/codebrowser.css")
        frag.add_css(unicode(css_str))
	

        js_str = pkg_resources.resource_string(__name__, "static/js/src/codebrowser_view.js")
        frag.add_javascript(unicode(js_str))
        js_str = pkg_resources.resource_string(__name__, "static/js/src/generate.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('CodeBrowserBlock')

        return frag

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        html_str = pkg_resources.resource_string(__name__, "static/html/codebrowser_edit.html")
        src = self.src or ''
        frag = Fragment(unicode(html_str).format(width=self.width, height=self.height))

        js_str = pkg_resources.resource_string(__name__, "static/js/src/codebrowser_edit.js")
        frag.add_javascript(unicode(js_str))
        frag.initialize_js('CodeBrowserBlock')

        return frag

    @XBlock.json_handler
    def generate(self, data, suffix=""):
      	"""
        generate static file for codebrowse
        """
    	student_id = self.runtime.anonymous_student_id
	real_user = self.runtime.get_real_user(self.runtime.anonymous_student_id)
	username = real_user.username
	lab = data["lab"]
    	os.system("/edx/var/edxapp/staticfiles/xblock-script/generator.sh "  + student_id + " " + username + " " + lab)
    	
    	return {"result": True}
    	
    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.width = data.get('width')
        self.height = data.get('height')
        return {'result': 'success'}


