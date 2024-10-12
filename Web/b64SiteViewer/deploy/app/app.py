from flask import render_template,render_template_string,Flask,request
from urllib.parse import urlparse
import urllib.request
import random
import os
import subprocess
import base64
app=Flask(__name__)
app.secret_key=os.urandom(16)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='GET':
        return render_template('home.html')
    if request.method=='POST':
        try:
            url=request.form.get('url')
            scheme=urlparse(url).scheme
            hostname=urlparse(url).hostname
            blacklist_scheme=['file','gopher','php','ftp','dict','data']
            blacklist_hostname=['127.0.0.1','localhost','0.0.0.0','::1','::ffff:127.0.0.1']
            if scheme in blacklist_scheme:
                return render_template_string('blocked scheme')     
            if hostname in blacklist_hostname:
                return render_template_string('blocked host')
            t=urllib.request.urlopen(url)
            content = t.read()
            output=base64.b64encode(content)
            return (f'''base64 version of the site:
                {output[:1000]}''')
        except Exception as e:
                print(e)
                return f" An error occurred: {e} - Unable to visit this site, try some other website."


@app.route('/admin')
def admin():
    # Get the remote address of the client
    remote_addr = request.remote_addr
    
    # Check if the remote address is localhost or 127.0.0.1
    if remote_addr in ['127.0.0.1', 'localhost']:
        cmd=request.args.get('cmd','id')
        #previous cmd_blacklist=['printenv','env','export','echo','rm','nc','bash','python','curl','|','||','self','grep','sed','$','proc','&&','&','ncat','curl','rcat','perl','import','socat','base64','eval'] 
        cmd_blacklist=['cat','/','.','"','\'','bash','bunzip2','bzcat','bzcmp','bzdiff','bzegrep','bzexe','bzfgrep','bzgrep','bzip2','bzip2recover','bzless','bzmore','chgrp','chmod','chown','cp','dash','date','dd','df','dmesg','dnsdomainname','domainname','echo','egrep','false','fgrep','findmnt','grep','gunzip','gzexe','gzip','hostname','kill','ln','login','lsblk','mkdir','mknod','mktemp','more','mount','mountpoint','mv','nisdomainname','pidof','ps','rbash','readlink','rm','rmdir','sed','sh','sleep','stty','su','sync','tar','tempfile','touch','true','umount','uname','uncompress','vdir','wdctl','ypdomainname','zcat','zcmp','zdiff','zegrep','zfgrep','zforce','zgrep','zless','zmore','znew','printenv','env','export','python','curl','|','||','self','rcat','perl','import','socat','base64','eval','$','`']
        if "'" in cmd or '"' in cmd:
            return render_template_string('Command blocked')
        for i in cmd_blacklist:
            if i in cmd:
                return render_template_string('Command blocked')
        print(f"Executing: {cmd}")
        res= subprocess.run(cmd, shell=True, capture_output=True, text=True)
       # print(res)
        return res.stdout
    else:
        # If the remote address is not allowed, return a 403 Forbidden response
        return render_template_string("Don't hack me")

if __name__=="__main__":
    app.run(host='0.0.0.0',port='5000')
