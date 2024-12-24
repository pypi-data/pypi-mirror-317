import textwrap


def get_context_clean(context_raw):
    context = {
        'pid':                  context_raw['pid'],
        'layout':               context_raw['layout_id'],
        # 'title':                truncatechars(context_raw['title'], 35).upper(),
        'data_inicio':          context_raw['data_inicio'],
        'data_conclusao':       context_raw['data_conclusao'],
        'customer_name':        get_cliente_nome(context_raw),
        'customer_contact':     get_cliente_contato(context_raw),
        'responsible_name':     get_responsavel_nome(context_raw),
        'responsible_contact':  get_responsavel_contato(context_raw),
        'body_base64':          context_raw['body_image_base64'],
        'logo_base64':          context_raw['logo_image_base64'],
        'financial':            context_raw['financeiro'].upper().strip(),
        'shipping':             context_raw['shipping'],
    }
    return context


def get_cliente_nome(context_raw):
    cliente_nome = context_raw['cliente_nome']
    customer_name = 'CLIENTE: {}'.format(cliente_nome).upper()
    customer_name = truncatechars(customer_name, 60)
    customer_name = customer_name.strip()
    return customer_name


def get_cliente_contato(context_raw):
    cliente_contato = context_raw['cliente_contato']
    customer_contact = 'CONTATO: {}'.format(cliente_contato)
    customer_contact = customer_contact
    customer_contact = customer_contact.strip()
    return customer_contact


def get_responsavel_nome(context_raw):
    responsavel_nome = context_raw['responsavel_nome']
    responsavel_nome = truncatechars(responsavel_nome, 44)
    responsavel_nome = responsavel_nome.strip()
    return responsavel_nome


def get_responsavel_contato(context_raw):
    responsavel_contato = context_raw['responsavel_contato']
    responsavel_contato = 'CONTATO: {}'.format(responsavel_contato).upper()
    responsavel_contato = responsavel_contato
    responsavel_contato = responsavel_contato.strip()
    return responsavel_contato


def truncatechars(string, width=10):
    return textwrap.shorten(string, width=width, placeholder="...")