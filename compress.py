

import os



os.chdir("./")


input_dir = "./input"
output_dir = "./output"

tmp_dir = "./tmp"


def to_mp4(input_file, output_file):
    os.system("mkdir -p %s" % tmp_dir)

    cmd = "convert %s -coalesce %s/xx_%%05d.png" % (input_file, tmp_dir)
    os.system(cmd)
    os.system("ffmpeg -r 6 -i %s/xx_%%05d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p %s"% (tmp_dir, output_file))
    os.system("rm -rf %s/" % tmp_dir)


processed_files = []

os.system("rm -rf %s/*" % output_dir)

for f in os.listdir(input_dir):
    input_f = os.path.join(input_dir, f)
    output_f = os.path.join(output_dir, f)
    output_f = output_f.replace(".gif", ".mp4")

    to_mp4(input_f, output_f)

    input_file_size = os.path.getsize(input_f)
    output_file_size = os.path.getsize(output_f)

    result = 100.0 - float(output_file_size)/float(input_file_size) * 100

    processed_files.append((input_f, input_file_size, output_f, output_file_size, result))


html_tpl_begin = "<!DOCTYPE html><html><head></head><body>"
html_tpl_end = "</body></html>"

resulting_html = html_tpl_begin
for r in processed_files:
    resulting_html += "<div>"
    resulting_html +=   '<img src="%s"/>' % r[0]
    resulting_html +=   '<h3> Size: ' + str(r[1]/(1024*1024.0)) + ' MB</h3>'
    resulting_html += '<video autoplay=true loop=true><source src="%s" type="video/mp4"/></video>' % r[2]
    resulting_html += '<h3> Size: ' + str(r[3]/(1024*1024.0)) + ' MB</h3>'
    resulting_html += '<h1> Compression: - ' + str(r[4]) + '%</h1>'
    resulting_html += "</div>"

resulting_html += html_tpl_end

with open("./index.html", "w") as f:
    f.write(resulting_html)

print("\n".join([str(r) for r in processed_files]))


