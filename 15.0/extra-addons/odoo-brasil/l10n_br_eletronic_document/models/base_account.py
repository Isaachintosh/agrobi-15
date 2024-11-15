from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
import re

from erpbrasil.base.fiscal.ie import validar as validar_ie

class NfeCFOP(models.Model):
    """CFOP - Código Fiscal de Operações e Prestações"""
    _name = 'nfe.cfop'
    _description = 'CFOP'

    code = fields.Char('Código', size=4, required=True)
    name = fields.Char('Nome', size=256, required=True)
    small_name = fields.Char('Nome Reduzido', size=32, required=True)
    description = fields.Text('Descrição')
    type = fields.Selection([('input', 'Entrada'),
                             ('output', 'Saída')],
                            'Tipo', required=True)
    parent_id = fields.Many2one(
        'nfe.cfop', 'CFOP Pai')
    child_ids = fields.One2many(
        'nfe.cfop', 'parent_id', 'CFOP Filhos')
    internal_type = fields.Selection(
        [('view', u'Visualização'), ('normal', 'Normal')],
        'Tipo Interno', required=True, default='normal')

    _sql_constraints = [
        ('nfe_cfop_code_uniq', 'unique (code)',
            'Já existe um CFOP com esse código !')
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s - %s" % (rec.code, rec.name or '')))
        return result


class AccountCNAE(models.Model):
    _name = 'account.cnae'
    _description = 'Cadastro de CNAE'

    code = fields.Char('Código', size=16, required=True)
    name = fields.Char('Descrição', size=64, required=True)
    version = fields.Char('Versão', size=16, required=True)
    parent_id = fields.Many2one('account.cnae', 'CNAE Pai')
    child_ids = fields.One2many(
        'account.cnae', 'parent_id', 'CNAEs Filhos')
    internal_type = fields.Selection(
        [('view', u'Visualização'), ('normal', 'Normal')],
        'Tipo Interno', required=True, default='normal')

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([('code', operator, name)] + args, limit=limit)
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit=limit)
        return recs.name_get()

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, "%s - %s" % (rec.code, rec.name or '')))
        return result


class ImportDeclaration(models.Model):
    _name = 'nfe.import.declaration'
    _description = "Declaração de Importação"

    move_id = fields.Many2one(
        'account.move', 'Fatura',
        ondelete='cascade', index=True)
    eletronic_document_line_id = fields.Many2one(
        'eletronic.document.line', 'Linha de Documento Eletrônico',
        ondelete='cascade', index=True)

    name = fields.Char('Número da DI', size=10, required=True)
    date_registration = fields.Date('Data de Registro', required=True)
    state_id = fields.Many2one(
        'res.country.state', 'Estado',
        domain="[('country_id.code', '=', 'BR')]", required=True)
    location = fields.Char('Local', required=True, size=60)
    date_release = fields.Date('Data de Liberação', required=True)
    type_transportation = fields.Selection([
        ('1', '1 - Marítima'),
        ('2', '2 - Fluvial'),
        ('3', '3 - Lacustre'),
        ('4', '4 - Aérea'),
        ('5', '5 - Postal'),
        ('6', '6 - Ferroviária'),
        ('7', '7 - Rodoviária'),
        ('8', '8 - Conduto / Rede Transmissão'),
        ('9', '9 - Meios Próprios'),
        ('10', '10 - Entrada / Saída ficta'),
    ], 'Transporte Internacional', required=True, default="1")
    afrmm_value = fields.Float(
        'Valor da AFRMM', digits='Account', default=0.00)
    type_import = fields.Selection([
        ('1', '1 - Importação por conta própria'),
        ('2', '2 - Importação por conta e ordem'),
        ('3', '3 - Importação por encomenda'),
    ], 'Tipo de Importação', default='1', required=True)
    thirdparty_cnpj = fields.Char('CNPJ', size=18)
    thirdparty_state_id = fields.Many2one(
        'res.country.state', 'Estado Parceiro',
        domain="[('country_id.code', '=', 'BR')]")
    exporting_code = fields.Char(
        'Código do Exportador', required=True, size=60)
    line_ids = fields.One2many(
        'nfe.import.declaration.line',
        'import_declaration_id', 'Linhas da DI')


class ImportDeclarationLine(models.Model):
    _name = 'nfe.import.declaration.line'
    _description = "Linha da declaração de importação"

    import_declaration_id = fields.Many2one(
        'nfe.import.declaration', 'DI', ondelete='cascade')
    sequence = fields.Integer('Sequência', default=1, required=True)
    name = fields.Char('Adição', size=3, required=True)
    manufacturer_code = fields.Char(
        'Código do Fabricante', size=60, required=True)
    amount_discount = fields.Float(
        string='Valor', digits='Account', default=0.00)
    drawback_number = fields.Char('Número Drawback', size=11)


class NfeRelatedDocumento(models.Model):
    _name = 'nfe.related.document'
    _description = "Documentos Relacionados"

    move_related_id = fields.Many2one(
        'account.move', 'Fatura Referenciada', ondelete='cascade')
    eletronic_document_id = fields.Many2one(
        'eletronic.document', 'Documento Eletrônico', ondelete='cascade')
    document_type = fields.Selection(
        [('nf', 'NF'), ('nfe', 'NF-e'), ('cte', 'CT-e'),
            ('nfrural', 'NF Produtor'), ('cf', 'Cupom Fiscal')],
        'Tipo Documento', required=True)
    access_key = fields.Char('Chave de Acesso', size=44)
    serie = fields.Char(u'Série', size=12)
    internal_number = fields.Char(u'Número', size=32)
    state_id = fields.Many2one('res.country.state', 'Estado',
                               domain="[('country_id.code', '=', 'BR')]")
    cnpj_cpf = fields.Char('CNPJ/CPF', size=18)
    cpfcnpj_type = fields.Selection(
        [('cpf', 'CPF'), ('cnpj', 'CNPJ')], 'Tipo Doc.',
        default='cnpj')
    inscr_est = fields.Char('Inscr. Estadual/RG', size=16)
    date = fields.Date('Data')

    @api.constrains('cnpj_cpf')
    def _check_cnpj_cpf(self):
        check_cnpj_cpf = True
        if self.cnpj_cpf:
            if self.cpfcnpj_type == 'cnpj':
                if not self.validar_cnpj(self.cnpj_cpf):
                    check_cnpj_cpf = False
            elif not self.validar_cpf(self.cnpj_cpf):
                check_cnpj_cpf = False
        if not check_cnpj_cpf:
            raise UserError(_('CNPJ/CPF do documento relacionado é invalido!'))

    @api.constrains('inscr_est')
    def _check_ie(self):
        check_ie = True
        if self.inscr_est:
            uf = self.state_id and self.state_id.code.lower() or ''
            try:
                mod = __import__('odoo.addons.l10n_br_base.tools.fiscal',
                                 globals(), locals(), 'fiscal')

                validate = getattr(mod, 'validate_ie_%s' % uf)
                if not validate(self.inscr_est):
                    check_ie = False
            except AttributeError:
                if not validar_ie(uf, self.inscr_est):
                    check_ie = False
        if not check_ie:
            raise UserError(
                _('Inscrição Estadual do documento fiscal inválida!'))

    def translate_document_type(self, code):
        if code == '55':
            return 'nfe'
        elif code == '04':
            return 'nfrural'
        elif code == '57':
            return 'cte'
        elif code in ('2B', '2C', '2D'):
            return 'cf'
        else:
            return 'nf'

    def check_cnpj_cpf(self, env, cnpj_cpf_value, country):
        """
        Check CNPJ or CPF is valid using erpbrasil library
        :param env:
        :param cnpj_cpf_value:
        :param country:
        :return:
        """
        if env and cnpj_cpf_value and country:
            if country == env.ref("base.br"):
                disable_cpf_cnpj_validation = env["ir.config_parameter"].sudo().get_param(
                    "l10n_br_base.disable_cpf_cnpj_validation", default=False
                ) or env.context.get("disable_cpf_cnpj_validation")

                if not disable_cpf_cnpj_validation:
                    if not self.validar(cnpj_cpf_value):
                        # Removendo . / - para diferenciar o CNPJ do CPF
                        # 62.228.384/0001-51 -CNPJ
                        # 62228384000151 - CNPJ
                        # 765.865.078-12 - CPF
                        # 76586507812 - CPF
                        document = "CPF"
                        if (
                            len("".join(char for char in cnpj_cpf_value if char.isdigit()))
                            == 14
                        ):
                            document = "CNPJ"

                        raise ValidationError(
                            _(
                                "%(d_type)s %(d_id)s is invalid!",
                                d_type=document,
                                d_id=cnpj_cpf_value,
                            )
                        )

    def validar(self, cnpj_cpf=None):
        """Função básica para validação de um CNPJ ou CPF depedendo da
        quantidade de digitos (sem acentuação), caso a string tenha 14 digitos
        será considerado como um CNPJ, caso tenha 11 será considerado como um CPF.
        :Parameters:
        - 'cnpj_cpf': CNPJ ou CPF para ser validado.
        :Return: True or False
        """
        if not cnpj_cpf:
            return
        cnpj_cpf = re.sub("[^0-9]", "", cnpj_cpf)

        if len(cnpj_cpf) == 14:
            return self.validar_cnpj(cnpj_cpf)

        if len(cnpj_cpf) == 11:
            return self.validar_cpf(cnpj_cpf)
    
    def validar_cnpj(self, cnpj):
        """Rotina para validação do CNPJ - Cadastro Nacional
        de Pessoa Juridica.
        :param string cnpj: CNPJ para ser validado
        :return bool: True or False
        """
        # Limpando o cnpj
        if not cnpj.isdigit():
            cnpj = re.sub("[^0-9]", "", cnpj)

        # verificando o tamano do  cnpj
        if len(cnpj) != 14:
            return False

        # Pega apenas os 12 primeiros dígitos do CNPJ e gera os digitos
        cnpj = list(map(int, cnpj))
        novo = cnpj[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        # Se o número gerado coincidir com o número original, é válido
        if novo == cnpj:
            return True

        return False


    def validar_cpf(cpf):
        """Rotina para validação do CPF - Cadastro Nacional
        de Pessoa Física.
        :Return: True or False
        :Parameters:
        - 'cpf': CPF to be validate.
        """
        # Limpando o cpf
        if not cpf.isdigit():
            cpf = re.sub("[^0-9]", "", cpf)

        if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
            return False

        # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
        cpf = list(map(int, cpf))
        novo = cpf[:9]

        while len(novo) < 11:
            r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)

        # Se o número gerado coincidir com o número original, é válido
        if novo == cpf:
            return True
        return False


class NfeFiscalObservation(models.Model):
    _name = 'nfe.fiscal.observation'
    _description = 'Mensagen Documento Eletrônico'
    _order = 'sequence'

    sequence = fields.Integer('Sequência', default=1, required=True)
    name = fields.Char('Descrição', required=True, size=50)
    message = fields.Text('Mensagem', required=True)
    tipo = fields.Selection([('fiscal', 'Observação Fiscal'),
                             ('observacao', 'Observação')], string="Tipo")
    tipo_produto = fields.Selection(
        [("product", "Produto"), ("service", "Serviço")],
        string="Tipo Produto",
    )