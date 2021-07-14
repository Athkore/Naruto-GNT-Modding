'''
SEQKing
Allows you to generate HTML reports from a lua SEQ log.
The report will show which instructions in a SEQ file were executed.
The logs are generated by seq_reader_gnt4.lua
'''
import os
import sys

def main():
    ''' Main function, responsible for parsing args and running the appropriate tool. '''
    check_args()
    write_html_report()

def check_args():
    ''' Checks that the program arguments are valid. '''
    if len(sys.argv) < 3:
        print('SEQKing')
        print('Allows you to generate HTML reports from a lua SEQ log.')
        print('The report will show which instructions in a SEQ file were executed.')
        print('These logs are generated by seq_reader_gnt4.lua')
        print('Usage:')
        print('python seq_path_report.py {log file} {seq file}\n')
        print('Example:')
        print('python seq_path_report.py D:/test.log D:/GNT/uncompressed/files/game/game00.seq')
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print(sys.argv[1] + ' is not a valid file.')
        sys.exit(1)
    if not os.path.isfile(sys.argv[2]):
        print(sys.argv[2] + ' is not a valid file.')
        sys.exit(1)

def write_html_report():
    ''' Writes the HTML report to an output path. '''
    html = get_html_header()
    html += get_html_body()
    output_path = get_output_path()
    with open(output_path, 'w') as output_file:
        output_file.write(html)

def get_html_header():
    ''' Returns the HTML header. '''
    html = '<!DOCTYPE html>'
    html += '<head>'
    html += '<meta charset="utf-8">'
    html += '<meta name="viewport" content="width=device-width, initial-scale=1">'
    html += '<link rel="preconnect" href="https://fonts.gstatic.com">'
    html += '<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap"'
    html += 'rel="stylesheet">'
    html += '<title>SEQKing Report</title>'
    html += '<style>'
    html += 'body {'
    html += 'background-color: #121212;'
    html += 'color: white;'
    html += 'font-family: "Roboto Mono", monospace;'
    html += '}'
    html += 'p {'
    html += 'opacity: 0.9;'
    html += '}'
    html += '.a {'
    html += 'background-color: #000080;'
    html += '}'
    html += '.b {'
    html += 'color: cyan;'
    html += '}'
    html += '</style>'
    html += '</head>'
    return html

def get_html_body():
    ''' Returns the HTML body. '''
    html = '<body>'
    html += '<h1>SEQKing Report: '
    html += os.path.basename(sys.argv[1])
    html += ' -> '
    html += os.path.basename(sys.argv[2])
    html += '</h1>'
    html += get_html_content()
    html += '</body>'
    html += '</html>'
    return html

def get_html_content():
    ''' Returns the actual content of the HTML report. '''
    log_file_path = sys.argv[1]
    seq_file_path = sys.argv[2].replace('\\', '/')
    with open(log_file_path, 'r') as log_file:
        log = log_file.readlines()
    offsets = set()
    for line in log:
        if seq_file_path.endswith(line[0:15]):
            offsets.add(int(line[17:25], 16))
    with open(seq_file_path, 'rb') as seq_file:
        data = seq_file.read()
    i = 0
    html = '<p>'
    html += '<span class="b">00000000</span> '
    while i < len(data):
        value = int.from_bytes(data[i:i+4], byteorder='big')
        if i in offsets:
            html += '<span class="a">'
            html += '{:08x}'.format(value)
            html += '</span> '
        else:
            html += '{:08x} '.format(value)
        i += 4
        if i % 32 == 0:
            #sys.exit(1)
            html += '</p><p>'
            html += '<span class="b">{:08x}</span> '.format(i)
    html += '</p>'
    return html

def get_output_path():
    ''' Returns the output path parameter or otherwise the log file with an html extension. '''
    if len(sys.argv) > 3:
        return sys.argv[3]
    return os.path.splitext(sys.argv[1])[0]+'.html'

if __name__ == "__main__":
    main()
