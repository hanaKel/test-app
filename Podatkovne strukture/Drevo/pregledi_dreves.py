# =============================================================================
# Pregledi dreves
#
# V vseh spodnjih primerih delovanja funkcij je `d` dvojiško drevo na spodnji
# sliki:
# 
#          5
#        /   \
#       3     2
#      /     / \
#     1     6   9
# 
# *Namig:* spomnite se ukazov `yield` in `yield from`.
# =====================================================================@029256=
# 1. podnaloga
# Sestavite generator `premi_pregled(drevo)`, ki vrača podatke v vozliščih
# drevesa v _premem vrstnem redu_ (pre-order). To pomeni, da najprej obiščemo
# koren drevesa, nato levo poddrevo in na koncu še desno poddrevo. Vozlišča
# poddreves obiskujemo po enakem pravilu. Zgled:
# 
#     >>> [x for x in premi_pregled(d)]
#     [5, 3, 1, 2, 6, 9]
# =============================================================================

from drevo import *

def premi_pregled(d):
    if d.prazno:
        return d()
    sez = [d.podatek]
    sez.append(premi_pregled(d.levo))
    sez.append(premi_pregled(d.desno))
    yield d.podatek
    
# =====================================================================@029257=
# 2. podnaloga
# Sestavite generator `vmesni_pregled(drevo)`, ki vrača podatke v vozliščih
# drevesa v _vmesnem vrstnem redu_ (in-order). To pomeni, da najprej obiščemo
# levo poddrevo, nato koren drevesa in na koncu še desno poddrevo. Vozlišča
# poddreves obiskujemo po enakem pravilu. Zgled:
# 
#     >>> [x for x in vmesni_pregled(d)]
#     [1, 3, 5, 6, 2, 9]
# =============================================================================

# =====================================================================@029258=
# 3. podnaloga
# Sestavite generator `obratni_pregled(drevo)`, ki vrača podatke v vozliščih
# drevesa v _obratnem vrstnem redu_ (post-order). To pomeni, da najprej
# obiščemo levo poddrevo, nato desno poddrevo in na koncu še koren drevesa.
# Vozlišča poddreves obiskujemo po enakem pravilu. Zgled:
# 
#     >>> [x for x in obratni_pregled(d)]
#     [1, 3, 6, 9, 2, 5]
# =============================================================================

# =====================================================================@029259=
# 4. podnaloga
# Sestavite generator `pregled_po_nivojih(drevo)`, ki vrača podatke v vozliščih
# drevesa _po nivojih_ (level-order). To pomeni, da najprej obiščemo koren,
# nato vsa vozlišča, ki so na globini 1, nato vsa vozlišča, ki so na globini 2
# itn. Vsa vozlišča na isti globini naštejemo od leve proti desni. Zgled:
# 
#     >>> [x for x in pregled_po_nivojih(d)]
#     [5, 3, 2, 1, 6, 9]
# =============================================================================





































































































# ============================================================================@

'Če vam Python sporoča, da je v tej vrstici sintaktična napaka,'
'se napaka v resnici skriva v zadnjih vrsticah vaše kode.'

'Kode od tu naprej NE SPREMINJAJTE!'


















































import json, os, re, sys, shutil, traceback, urllib.error, urllib.request


import io, sys
from contextlib import contextmanager

class VisibleStringIO(io.StringIO):
    def read(self, size=None):
        x = io.StringIO.read(self, size)
        print(x, end='')
        return x

    def readline(self, size=None):
        line = io.StringIO.readline(self, size)
        print(line, end='')
        return line


class Check:
    parts = None
    current_part = None
    part_counter = None

    @staticmethod
    def has_solution(part):
        return part['solution'].strip() != ''

    @staticmethod
    def initialize(parts):
        Check.parts = parts
        for part in Check.parts:
            part['valid'] = True
            part['feedback'] = []
            part['secret'] = []

    @staticmethod
    def part():
        if Check.part_counter is None:
            Check.part_counter = 0
        else:
            Check.part_counter += 1
        Check.current_part = Check.parts[Check.part_counter]
        return Check.has_solution(Check.current_part)

    @staticmethod
    def feedback(message, *args, **kwargs):
        Check.current_part['feedback'].append(message.format(*args, **kwargs))

    @staticmethod
    def error(message, *args, **kwargs):
        Check.current_part['valid'] = False
        Check.feedback(message, *args, **kwargs)

    @staticmethod
    def clean(x, digits=6, typed=False):
        t = type(x)
        if t is float:
            x = round(x, digits)
            # Since -0.0 differs from 0.0 even after rounding,
            # we change it to 0.0 abusing the fact it behaves as False.
            v = x if x else 0.0
        elif t is complex:
            v = complex(Check.clean(x.real, digits, typed), Check.clean(x.imag, digits, typed))
        elif t is list:
            v = list([Check.clean(y, digits, typed) for y in x])
        elif t is tuple:
            v = tuple([Check.clean(y, digits, typed) for y in x])
        elif t is dict:
            v = sorted([(Check.clean(k, digits, typed), Check.clean(v, digits, typed)) for (k, v) in x.items()])
        elif t is set:
            v = sorted([Check.clean(y, digits, typed) for y in x])
        else:
            v = x
        return (t, v) if typed else v

    @staticmethod
    def secret(x, hint=None, clean=None):
        clean = Check.get('clean', clean)
        Check.current_part['secret'].append((str(clean(x)), hint))

    @staticmethod
    def equal(expression, expected_result, clean=None, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        actual_result = eval(expression, global_env)
        if clean(actual_result) != clean(expected_result):
            Check.error('Izraz {0} vrne {1!r} namesto {2!r}.',
                        expression, actual_result, expected_result)
            return False
        else:
            return True

    @staticmethod
    def approx(expression, expected_result, tol=1e-6, env=None, update_env=None):
        try:
            import numpy as np
        except ImportError:
            Check.error('Namestiti morate numpy.')
            return False
        if not isinstance(expected_result, np.ndarray):
            Check.error('Ta funkcija je namenjena testiranju za tip np.ndarray.')

        if env is None:
            env = dict()
        env.update({'np': np})
        global_env = Check.init_environment(env=env, update_env=update_env)
        actual_result = eval(expression, global_env)
        if type(actual_result) is not type(expected_result):
            Check.error("Rezultat ima napačen tip. Pričakovan tip: {}, dobljen tip: {}.",
                        type(expected_result).__name__, type(actual_result).__name__)
            return False
        exp_shape = expected_result.shape
        act_shape = actual_result.shape
        if exp_shape != act_shape:
            Check.error("Obliki se ne ujemata. Pričakovana oblika: {}, dobljena oblika: {}.", exp_shape, act_shape)
            return False
        try:
            np.testing.assert_allclose(expected_result, actual_result, atol=tol, rtol=tol)
            return True
        except AssertionError as e:
            Check.error("Rezultat ni pravilen." + str(e))
            return False

    @staticmethod
    def run(statements, expected_state, clean=None, env=None, update_env=None):
        code = "\n".join(statements)
        statements = "  >>> " + "\n  >>> ".join(statements)
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        exec(code, global_env)
        errors = []
        for (x, v) in expected_state.items():
            if x not in global_env:
                errors.append('morajo nastaviti spremenljivko {0}, vendar je ne'.format(x))
            elif clean(global_env[x]) != clean(v):
                errors.append('nastavijo {0} na {1!r} namesto na {2!r}'.format(x, global_env[x], v))
        if errors:
            Check.error('Ukazi\n{0}\n{1}.', statements,  ";\n".join(errors))
            return False
        else:
            return True

    @staticmethod
    @contextmanager
    def in_file(filename, content, encoding=None):
        encoding = Check.get('encoding', encoding)
        with open(filename, 'w', encoding=encoding) as f:
            for line in content:
                print(line, file=f)
        old_feedback = Check.current_part['feedback'][:]
        yield
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n    '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodni datoteki {0} z vsebino\n  {1}\nso se pojavile naslednje napake:\n- {2}', filename, '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    @contextmanager
    def input(content, visible=None):
        old_stdin = sys.stdin
        old_feedback = Check.current_part['feedback'][:]
        try:
            with Check.set_stringio(visible):
                sys.stdin = Check.get('stringio')('\n'.join(content) + '\n')
                yield
        finally:
            sys.stdin = old_stdin
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n  '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodu\n  {0}\nso se pojavile naslednje napake:\n- {1}', '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    def out_file(filename, content, encoding=None):
        encoding = Check.get('encoding', encoding)
        with open(filename, encoding=encoding) as f:
            out_lines = f.readlines()
        equal, diff, line_width = Check.difflines(out_lines, content)
        if equal:
            return True
        else:
            Check.error('Izhodna datoteka {0}\n  je enaka{1}  namesto:\n  {2}', filename, (line_width - 7) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def output(expression, content, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exec(expression, global_env)
        finally:
            output = sys.stdout.getvalue().rstrip().splitlines()
            sys.stdout = old_stdout
        equal, diff, line_width = Check.difflines(output, content)
        if equal:
            return True
        else:
            Check.error('Program izpiše{0}  namesto:\n  {1}', (line_width - 13) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def difflines(actual_lines, expected_lines):
        actual_len, expected_len = len(actual_lines), len(expected_lines)
        if actual_len < expected_len:
            actual_lines += (expected_len - actual_len) * ['\n']
        else:
            expected_lines += (actual_len - expected_len) * ['\n']
        equal = True
        line_width = max(len(actual_line.rstrip()) for actual_line in actual_lines + ['Program izpiše'])
        diff = []
        for out, given in zip(actual_lines, expected_lines):
            out, given = out.rstrip(), given.rstrip()
            if out != given:
                equal = False
            diff.append('{0} {1} {2}'.format(out.ljust(line_width), '|' if out == given else '*', given))
        return equal, diff, line_width

    @staticmethod
    def init_environment(env=None, update_env=None):
        global_env = globals()
        if not Check.get('update_env', update_env):
            global_env = dict(global_env)
        global_env.update(Check.get('env', env))
        return global_env

    @staticmethod
    def generator(expression, expected_values, should_stop=None, further_iter=None, clean=None, env=None, update_env=None):
        from types import GeneratorType
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        gen = eval(expression, global_env)
        if not isinstance(gen, GeneratorType):
            Check.error("Izraz {0} ni generator.", expression)
            return False

        try:
            for iteration, expected_value in enumerate(expected_values):
                actual_value = next(gen)
                if clean(actual_value) != clean(expected_value):
                    Check.error("Vrednost #{0}, ki jo vrne generator {1} je {2!r} namesto {3!r}.",
                                iteration, expression, actual_value, expected_value)
                    return False
            for _ in range(Check.get('further_iter', further_iter)):
                next(gen)  # we will not validate it
        except StopIteration:
            Check.error("Generator {0} se prehitro izteče.", expression)
            return False

        if Check.get('should_stop', should_stop):
            try:
                next(gen)
                Check.error("Generator {0} se ne izteče (dovolj zgodaj).", expression)
            except StopIteration:
                pass  # this is fine
        return True

    @staticmethod
    def summarize():
        for i, part in enumerate(Check.parts):
            if not Check.has_solution(part):
                print('{0}. podnaloga je brez rešitve.'.format(i + 1))
            elif not part['valid']:
                print('{0}. podnaloga nima veljavne rešitve.'.format(i + 1))
            else:
                print('{0}. podnaloga ima veljavno rešitev.'.format(i + 1))
            for message in part['feedback']:
                print('  - {0}'.format('\n    '.join(message.splitlines())))

    settings_stack = [{
        'clean': clean.__func__,
        'encoding': None,
        'env': {},
        'further_iter': 0,
        'should_stop': False,
        'stringio': VisibleStringIO,
        'update_env': False,
    }]

    @staticmethod
    def get(key, value=None):
        if value is None:
            return Check.settings_stack[-1][key]
        return value

    @staticmethod
    @contextmanager
    def set(**kwargs):
        settings = dict(Check.settings_stack[-1])
        settings.update(kwargs)
        Check.settings_stack.append(settings)
        try:
            yield
        finally:
            Check.settings_stack.pop()

    @staticmethod
    @contextmanager
    def set_clean(clean=None, **kwargs):
        clean = clean or Check.clean
        with Check.set(clean=(lambda x: clean(x, **kwargs))
                             if kwargs else clean):
            yield

    @staticmethod
    @contextmanager
    def set_environment(**kwargs):
        env = dict(Check.get('env'))
        env.update(kwargs)
        with Check.set(env=env):
            yield

    @staticmethod
    @contextmanager
    def set_stringio(stringio):
        if stringio is True:
            stringio = VisibleStringIO
        elif stringio is False:
            stringio = io.StringIO
        if stringio is None or stringio is Check.get('stringio'):
            yield
        else:
            with Check.set(stringio=stringio):
                yield


def _validate_current_file():
    def extract_parts(filename):
        with open(filename, encoding='utf-8') as f:
            source = f.read()
        part_regex = re.compile(
            r'# =+@(?P<part>\d+)=\s*\n' # beginning of header
            r'(\s*#( [^\n]*)?\n)+?'     # description
            r'\s*# =+\s*?\n'            # end of header
            r'(?P<solution>.*?)'        # solution
            r'(?=\n\s*# =+@)',          # beginning of next part
            flags=re.DOTALL | re.MULTILINE
        )
        parts = [{
            'part': int(match.group('part')),
            'solution': match.group('solution')
        } for match in part_regex.finditer(source)]
        # The last solution extends all the way to the validation code,
        # so we strip any trailing whitespace from it.
        parts[-1]['solution'] = parts[-1]['solution'].rstrip()
        return parts

    def backup(filename):
        backup_filename = None
        suffix = 1
        while not backup_filename or os.path.exists(backup_filename):
            backup_filename = '{0}.{1}'.format(filename, suffix)
            suffix += 1
        shutil.copy(filename, backup_filename)
        return backup_filename

    def submit_parts(parts, url, token):
        submitted_parts = []
        for part in parts:
            if Check.has_solution(part):
                submitted_part = {
                    'part': part['part'],
                    'solution': part['solution'],
                    'valid': part['valid'],
                    'secret': [x for (x, _) in part['secret']],
                    'feedback': json.dumps(part['feedback']),
                }
                if 'token' in part:
                    submitted_part['token'] = part['token']
                submitted_parts.append(submitted_part)
        data = json.dumps(submitted_parts).encode('utf-8')
        headers = {
            'Authorization': token,
            'content-type': 'application/json'
        }
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request, context=ctx)
        return json.loads(response.read().decode('utf-8'))

    def update_attempts(old_parts, response):
        updates = {}
        for part in response['attempts']:
            part['feedback'] = json.loads(part['feedback'])
            updates[part['part']] = part
        for part in old_parts:
            valid_before = part['valid']
            part.update(updates.get(part['part'], {}))
            valid_after = part['valid']
            if valid_before and not valid_after:
                wrong_index = response['wrong_indices'].get(str(part['part']))
                if wrong_index is not None:
                    hint = part['secret'][wrong_index][1]
                    if hint:
                        part['feedback'].append('Namig: {}'.format(hint))


    filename = os.path.abspath(sys.argv[0])
    file_parts = extract_parts(filename)
    Check.initialize(file_parts)

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjo2ODQ4LCJwYXJ0IjoyOTI1Nn0:1msScG:0j-wnS7hsv5yBUUCHTak-LoIWs8'
        try:
            test_data = [
                ('premi_pregled(Drevo(5, levo=Drevo(3, levo=Drevo(1)), desno=Drevo(2, levo=Drevo(6), desno=Drevo(9))))', [5, 3, 1, 2, 6, 9]),
                ('premi_pregled(Drevo())', []),
                ('premi_pregled(Drevo(3))', [3]),
                ('premi_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3)))', [5, 4, 2, 3]),
                ('premi_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3, levo=Drevo(4), desno=Drevo(4))))', [5, 4, 2, 3, 4, 4]),
                ('premi_pregled(Drevo(-2, levo=Drevo(4, desno=Drevo(21)), desno=Drevo(23, levo=Drevo(5, levo=Drevo(13, levo=Drevo(11)), desno=Drevo(24, levo=Drevo(6), desno=Drevo(9))), desno=Drevo(73, levo=Drevo(44), desno=Drevo(54)))))',
                 [-2, 4, 21, 23, 5, 13, 11, 24, 6, 9, 73, 44, 54]),
            ]
            for td in test_data:
                if not Check.generator(*td, should_stop=True):
                    break
            _drevesa = [Drevo(), Drevo()]
            for i in range(1, 12):
                _drevesa.append(Drevo(i, levo=_drevesa[-1], desno=_drevesa[-2]))
                Check.secret(list(premi_pregled(_drevesa[-1])))
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjo2ODQ4LCJwYXJ0IjoyOTI1N30:1msScG:-NKxAkiyCr1G0SmsCQowR73jFk4'
        try:
            test_data = [
                ('vmesni_pregled(Drevo(5, levo=Drevo(3, levo=Drevo(1)), desno=Drevo(2, levo=Drevo(6), desno=Drevo(9))))', [1, 3, 5, 6, 2, 9]),
                ('vmesni_pregled(Drevo())', []),
                ('vmesni_pregled(Drevo(3))', [3]),
                ('vmesni_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3)))', [4, 2, 5, 3]),
                ('vmesni_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3, levo=Drevo(4), desno=Drevo(4))))', [4, 2, 5, 4, 3, 4]),
                ('vmesni_pregled(Drevo(-2, levo=Drevo(4, desno=Drevo(21)), desno=Drevo(23, levo=Drevo(5, levo=Drevo(13, levo=Drevo(11)), desno=Drevo(24, levo=Drevo(6), desno=Drevo(9))), desno=Drevo(73, levo=Drevo(44), desno=Drevo(54)))))',
                 [4, 21, -2, 11, 13, 5, 6, 24, 9, 23, 44, 73, 54]),
            ]
            for td in test_data:
                if not Check.generator(*td, should_stop=True):
                    break
            _drevesa = [Drevo(), Drevo()]
            for i in range(1, 12):
                _drevesa.append(Drevo(i, levo=_drevesa[-1], desno=_drevesa[-2]))
                Check.secret(list(vmesni_pregled(_drevesa[-1])))
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjo2ODQ4LCJwYXJ0IjoyOTI1OH0:1msScG:HQbUz0Ke6PrGU5Sn1RvaY1Zij-Y'
        try:
            test_data = [
                ('obratni_pregled(Drevo(5, levo=Drevo(3, levo=Drevo(1)), desno=Drevo(2, levo=Drevo(6), desno=Drevo(9))))', [1, 3, 6, 9, 2, 5]),
                ('obratni_pregled(Drevo())', []),
                ('obratni_pregled(Drevo(3))', [3]),
                ('obratni_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3)))', [2, 4, 3, 5]),
                ('obratni_pregled(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3, levo=Drevo(4), desno=Drevo(4))))', [2, 4, 4, 4, 3, 5]),
                ('obratni_pregled(Drevo(-2, levo=Drevo(4, desno=Drevo(21)), desno=Drevo(23, levo=Drevo(5, levo=Drevo(13, levo=Drevo(11)), desno=Drevo(24, levo=Drevo(6), desno=Drevo(9))), desno=Drevo(73, levo=Drevo(44), desno=Drevo(54)))))',
                 [21, 4, 11, 13, 6, 9, 24, 5, 44, 54, 73, 23, -2] ),
            ]
            for td in test_data:
                if not Check.generator(*td, should_stop=True):
                    break
            _drevesa = [Drevo(), Drevo()]
            for i in range(1, 12):
                _drevesa.append(Drevo(i, levo=_drevesa[-1], desno=_drevesa[-2]))
                Check.secret(list(obratni_pregled(_drevesa[-1])))
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjo2ODQ4LCJwYXJ0IjoyOTI1OX0:1msScG:DiMuzgm8Er3NFT0zyrgBU4gWUSM'
        try:
            test_data = [
                ('pregled_po_nivojih(Drevo(5, levo=Drevo(3, levo=Drevo(1)), desno=Drevo(2, levo=Drevo(6), desno=Drevo(9))))', [5, 3, 2, 1, 6, 9]),
                ('pregled_po_nivojih(Drevo())', []),
                ('pregled_po_nivojih(Drevo(3))', [3]),
                ('pregled_po_nivojih(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3)))', [5, 4, 3, 2]),
                ('pregled_po_nivojih(Drevo(5, levo=Drevo(4, desno=Drevo(2)), desno=Drevo(3, levo=Drevo(4), desno=Drevo(4))))', [5, 4, 3, 2, 4, 4]),
                ('pregled_po_nivojih(Drevo(-2, levo=Drevo(4, desno=Drevo(21)), desno=Drevo(23, levo=Drevo(5, levo=Drevo(13, levo=Drevo(11)), desno=Drevo(24, levo=Drevo(6), desno=Drevo(9))), desno=Drevo(73, levo=Drevo(44), desno=Drevo(54)))))',
                 [-2, 4, 23, 21, 5, 73, 13, 24, 44, 54, 11, 6, 9]),
            ]
            for td in test_data:
                if not Check.generator(*td, should_stop=True):
                    break
            _drevesa = [Drevo(), Drevo()]
            for i in range(1, 12):
                _drevesa.append(Drevo(i, levo=_drevesa[-1], desno=_drevesa[-2]))
                Check.secret(list(pregled_po_nivojih(_drevesa[-1])))
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    print('Shranjujem rešitve na strežnik... ', end="")
    try:
        url = 'https://www.projekt-tomo.si/api/attempts/submit/'
        token = 'Token 451c2f2b636ce7933da1119326183eb68388d586'
        response = submit_parts(Check.parts, url, token)
    except urllib.error.URLError:
        message = ('\n'
                   '-------------------------------------------------------------------\n'
                   'PRI SHRANJEVANJU JE PRIŠLO DO NAPAKE!\n'
                   'Preberite napako in poskusite znova ali se posvetujte z asistentom.\n'
                   '-------------------------------------------------------------------\n')
        print(message)
        traceback.print_exc()
        print(message)
        sys.exit(1)
    else:
        print('Rešitve so shranjene.')
        update_attempts(Check.parts, response)
        if 'update' in response:
            print('Posodabljam datoteko... ', end="")
            backup_filename = backup(filename)
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(response['update'])
            print('Stara datoteka je bila preimenovana v {0}.'.format(backup_filename))
            print('Če se datoteka v urejevalniku ni osvežila, jo zaprite ter ponovno odprite.')
    Check.summarize()

if __name__ == '__main__':
    _validate_current_file()
