# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2017-2018 Sergio Corato.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
{
    'name': 'Ricevute bancarie accruement',
    'version': '8.0.1.0.0',
    'category': 'other',
    'author': 'Sergio Corato',
    'website': 'http://www.efatto.it',
    'description': 'Ricevute bancarie con processo di maturazione per valuta.'
    'Con questo modulo viene modificato il processo per rendere'
    ' possibili i seguenti passaggi: \n'
    '1. Creazione delle ri.ba. con emissione del flusso,\n'
    '2. Accettazione dell\'intero flusso ri.ba. emesso verso la'
    ' banca:'
    ' viene creata la registrazione di chiusura del credito'
    'v/il cliente e l\'entrata corrispondente usualmente nel '
    'conto "Effetti all\'incasso". Questo conto va configurato '
    'come "crediti" e contenendo data di scadenza e dettagli sul cliente,'
    '\è utile per la chiusura di bilancio,\n'
    '3. Registrazione di accredito del flusso: \è possibile farlo sia '
    'per l\'intero flusso o per una/più linee dalle distinte riba, oppure'
    ' per una/più righe dal menu linee riba. Viene creata una registrazione '
    'di accredito dell\'importo nel c/c, con corrispondente importo '
    'a debito nel conto ri.ba. all\'incasso. Questa registrazione è in '
    'sostanza un giroconto per l\'apertura del debito verso la banca, in '
    'corrispondenza dell\'anticipazione di credito ricevuta.\n'
    '4. Registrazione di maturazione a valuta per selezione di '
    'singole ri.ba. (eseguibile dalla vista elenco ri.ba.) o dell\'intero '
    'flusso, eseguibile dalla distinta ri.ba.. Viene riconciliato il partner'
    '\n',
    'license': 'AGPL-3',
    'depends': [
        'account_bank',
        'account_payment_term_month',
        'l10n_it_abicab',
        'l10n_it_ricevute_bancarie',
        'l10n_it_ricevute_bancarie_ext',
    ],
    'data': [
        'views/riba_view.xml',
        'views/wizard_accreditation.xml',
    ],
    'installable': True
}