"""
This is for figuring out how the scraped data will be written to a new webpage. The output is in htmlfiles
"""

import os
import json
import eyed3
from distutils.dir_util import copy_tree

def test1html():
    head = [
        '<!DOCTYPE html>',
        '<!--',
        'B.A.D. Website HTML',
        'Robert Bergers',
        '-->',
        '<html>',
        '<head>',
        '<meta charset="utf-8">'
        '<title>B.A.D. Website</title>',
        '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>',
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">',
        '<link rel="stylesheet" href="./css/styles.css">',
        '</head>'
    ]
    foot = [
        '</div>',    #Row
        '</div>',    #Container
        '</body>',
        '</html>'
    ]
    #View output: htmlfiles/test.html
    testfile = open('./htmlfiles/test.html', 'w')
    #Header
    for line in head:
        testfile.write(line + '\n')
    #Body
    testfile.write('<body>\n'
                   '<h6 id="copyright">© Robby Bergers 2018</h6>')
    #Topbar
    testfile.write('<div class="container-fluid topbar">\n'
                   '<div class="row">\n'
                   '<div class="col-md-12 sitetitle">\n'
                   '<h3>Bearer of Awesome Data</h3>\n'
                   '</div></div></div>')
    #Main content
    testfile.write('<div class="container-fluid">\n'
                   '<div class="row">\n'
                   '<div class="col-md-3"><h4><a href="https://www.nasa.gov/multimedia/imagegallery/iotd.html" target="_blank">NASA Images</a></h4></div>\n'
                   '<div class="col-md-3"><h4><a href="https://www.startalkradio.net/" target="_blank">StarTalk Podcast</a></h4>\n</div>\n'
                   '<div class="col-md-6"><h4><a href="https://www.youtube.com/user/ouramazingspace" target="_blank">Amazing Space</a></h4></div>\n'
                   '</div>\n'
                   '<div class="row">\n')
    #Image Files
    testfile.write('<div class="col col-sm-3 medial">\n')
    i = 0
    for filename in os.listdir('../docs/imgfiles/'):
        testfile.write('<div class="col-md-12 content"><img src="./imgfiles/' + filename + '"></div>\n')
    testfile.write('</div>\n')
    # MP3 Files
    testfile.write('<div class="col col-sm-3 medial">\n')
    i = 0
    for filename in os.listdir('../docs/mp3files'):
        if (i < 40):
            path = '../docs/mp3files/' + filename
            audio = eyed3.load(path)
            title = audio.tag.title
            testfile.write(
                '<div class="col-md-12 content"><h5>' + title + '</h5><span class="mask"><audio controls><source src="./mp3files/' + filename + '"></audio></span></div>\n')
            i += 1
        else:
            break
    testfile.write('</div>\n')
    #Video files
    testfile.write('<div class="col-sm-6 medial">\n')
    jsonobj = open('./JSON/video.json', 'r').read()
    videos = json.loads(jsonobj)
    for video in videos:
        url = videos[video]
        testfile.write('<iframe width="560" height="315" src="https://www.youtube.com/embed/' + url + '" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n')
    testfile.write('</div>')
    #Footer
    for line in foot:
        testfile.write(line + '\n')
    testfile.close()

def toSite():
    #Paths
    testpath = './htmlfiles/test.html'
    testcss = './htmlfiles/css/styles.css'
    sitepath = '../docs/index.html'
    sitecss = '../docs/css/styles.css'
    mp3from = './mp3files'
    mp3to = '../docs/mp3files'
    imgfrom = './imgfiles'
    imgto = '../docs/imgfiles'
    #HTML
    inputfile = open(testpath, 'r').read()
    sitefile = open(sitepath, 'w')
    sitefile.write(inputfile)
    sitefile.close()

if __name__ == '__main__':
    test1html()
    toSite()

"""
<iframe width="560" height="315" src="https://www.youtube.com/embed/[PASTE THE EXTENSION OF
YOUTUBE URL (the URL substring after '/watch?v=') HERE]" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
"""