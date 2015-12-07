#!python3.4
# BBCodeParser 1.0
# Written by Dylan5797 [https://dylan5797.github.io]

def parse_bbcode(bc):
    tokens_found = []
    current_text = ''
    parsing_tag = False
    for x in bc:
        if parsing_tag:
            current_text = current_text + x
            if x == ']':
                tokens_found.append({'id':'tag', 'value':current_text})
                parsing_tag = False
                current_text = ''
                continue
        else:
            if x[0] == '[':
                tokens_found.append({'id':'text', 'value':current_text})
                current_text = '['
                parsing_tag = True
                continue
            else:
                current_text = current_text + x
    tokens_found.append({'id':'text', 'value':current_text})
    def recur(tokens, dep=0):
        output = []
        if dep > 0:
            name = tokens[0]['value'][1:-1]
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
                if x['value'] == '[/' + name + ']':
                    break
            if x['id'] == 'text':
                output.append(x['value'])
            else:
                re = recur(bump, dep + 1)
                skip = re[1]
                output.append({'tag':x['value'], 'value':re[0]})
        if dep > 0:
            return [output, counted - 1]
        else:
            return output
    return recur(tokens_found)
