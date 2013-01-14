encoding = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'

def make_table(title, table):

    html = [encoding, '<table>']

    html.append('<tr>' + ''.join(['<th>%s</th>'%x for x in title]) + '</tr>')

    for line in table:

        html.append('<tr>' + ''.join(['<td>%s</td>'%x for x in line]) + '</tr>')

    html.append('</table>')

    return '\n'.join(html)       
    
