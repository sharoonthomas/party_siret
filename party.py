#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import Model, fields
from trytond.pyson import Eval
import luhn


class Party(Model):
    _name = 'party.party'

    siren = fields.Char('SIREN', select=1, states={
            'readonly': ~Eval('active', True),
            }, size=9, depends=['active'])

    def __init__(self):
        super(Party, self).__init__()
        self._constraints += [
            ('check_siren', 'invalid_siren'),
        ]
        self._error_messages.update({
            'invalid_siren': 'Invalid SIREN number!',
        })

    def check_siren(self, ids):
        '''
        Check validity of SIREN
        '''
        for party in self.browse(ids):
            if party.siren and not luhn.validate(party.siren):
                return False
        return True

Party()
