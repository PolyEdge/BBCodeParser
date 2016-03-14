#!python3.4
# BBCodeParser 1.0
# Written by Dylan5797 [https://dylan5797.github.io]

#!python3
formats = {
    "_default":{
        "style":"style",
        "id":"id",
        "key":"accesskey",
        "class":"class"
        },
    "url":{
        "html":"a",
        "keys":{
            "_":"href",
            "download":"download",
            }
        },
    "b":{
        "html":"b",
        "keys":{}
        },
    "em":{
        "html":"em"
        },
    "quote":{
        "html":"blockquote",
        "keys":{}
        },
    "break":{
        "html":"br",
        "keys":{}
        },
    "code":{
        "html":"code",
        "keys":{}
        },
    "h1":{
        "html":"h",
        "keys":{}
        },
    "h2":{
        "html":"h2",
        "keys":{}
        },
    "h3":{
        "html":"h3",
        "keys":{}
        },
    "h4":{
        "html":"h4",
        "keys":{}
        },
    "h5":{
        "html":"h5",
        "keys":{}
        },
    "h6":{
        "html":"h6",
        "keys":{}
        },
    "i":{
        "html":"i",
        "keys":{}
        },
    "olist":{
        "html":"ol",
        "keys":{
            "start":"start",
            "type":"type"
            }
        },
    "lquote":{
        "html":"q",
        "keys":{}
        },
    "s":{
        "html":"s",
        "keys":{}
        },
    "span":{
        "html":"span",
        "keys":{
            "color":"color",
            }
        },
    "sub":{
        "html":"sub",
        "keys":{}
        },
    "sup":{
        "html":"sup",
        "keys":{}
        },
    "table":{
        "html":"table",
        "keys":{}
        },
    "row":{
        "html":"tr",
        "keys":{}
        },
    "headrow":{
        "html":"th",
        "keys":{}
        },
    "cell":{
        "html":"td",
        "keys":{}
        },
    "u":{
        "html":"u",
        "keys":{}
        },
    "list":{
        "html":"ul",
        "keys":{}
        },
    "img":{
        "html":"img",
        "keys":{
            "hover":"alt",
            "height":"height",
            "width":"width",
            "url":"src"
            }
        }
}

# Syntax:
# [italic]italic[/italic]
def parse_bbcode(bc):
    tokens_found = []
    current_text = ''
    count = -1
    parsing_tag = False
    in_code = False
    code_init = False
    tag_depth = 0
    for x in bc:
        count += 1
        if parsing_tag:
            if x == '[':
                tag_depth += 1
            if tag_depth == 0:
                current_text = current_text + x
            if x == ']' and tag_depth == 0:
                current_text = current_text[1:-1]
                attr = {}
                for x in current_text.split():
                    try: attr[x.rsplit('=')[0]] = x.rsplit('=')[1]
                    except: pass
                tokens_found.append({'id':'tag', 'attributes':attr, 'value':current_text.split()[0].rsplit('=')[0]})
                parsing_tag = False
                current_text = ''
                continue
            elif x == ']':
                tag_depth -= 1
            if code_init:
                in_code = True
                code_init = False
        else:
            try: n1 = bc[count]; n2 = bc[count]
            except: n1 = ''; n2 = ''
            if x[0] == '[' and (not (n1 == '[' and n2 == ']')) and (not in_code):
                tag_depth = 0
                tokens_found.append({'id':'text', 'value':current_text})
                current_text = '['
                parsing_tag = True
                if bc[count:count+6] == '[code]':
                    code_init = True
                continue
            elif in_code and bc[count:count+7] == '[/code]':
                tag_depth = 0
                tokens_found.append({'id':'text', 'value':current_text})
                current_text = '['
                parsing_tag = True
                in_code = False
                continue                
            else:
                current_text = current_text + x
    tokens_found.append({'id':'text', 'value':current_text})
    def compile_tags(tokens, dep=0):
        output = []
        if dep > 0:
            name = tokens[0]['value']
        counted = 0
        skip = 0
        bump = ['']
        for x in tokens:
            bump.append(x)
        for x in tokens:
            counted = counted + 1
            bump = bump[1:]
            if skip > 0:
                skip = skip - 1
                continue
            if dep > 0 and len(bump) == len(tokens):
                continue
            if dep > 0:
                if x['value'] == '/' + name:
                    break
            if x['id'] == 'text':
                output.append(x['value'])
            else:
                re = compile_tags(bump, dep + 1)
                skip = re[1]
                output.append({'tag':x['value'], 'value':re[0], 'param':x['attributes']})
        if dep > 0:
            return [output, counted - 1]
        else:
            return output
    return compile_tags(tokens_found)

def convert_to_html(bc):
    def recurse(data):
        output = ''
        for x in data:
            if type(x) == str:
                output = output + x.replace('\n', '<br>')
            else:
                output = output + '<' + formats[x['tag']]['html'] + ''.join([(' ' + formats[x['tag']]['keys']['_'] + '="' + x['param'][y] + '"') for y in x['param'] if (y == x['tag']) and ('_' in formats[x['tag']]['keys'])] + [(' ' + formats[x['tag']]['keys'][y] + '="' + x['param'][y] + '"') for y in x['param'] if y in formats[x['tag']]['keys']] + [(' ' + formats['_default'][y] + '="' + x['param'][y] + '"') for y in x['param'] if y in formats['_default']]) + '>'
                output = output + recurse(x['value'])
                output = output + '</' + formats[x['tag']]['html'] + '>'
        return output
    return recurse(bc)
