from RFML.libs.NLP.CancelPrompt import CancelPrompt
from RFML.libs.NLP.NERGenerator import NERGenerator
from RFML.libs.core.CLI import CLI
from RFML.libs.core.DateTime import DateTime
from RFML.libs.core.Generator import Generator
from RFML.libs.core.Number import Number


class Nlp:
    ner = NERGenerator()
    prompt = CancelPrompt()


class rf:
    datetime = DateTime()
    nlp = Nlp()
    gen = Generator()
    cli = CLI()
    number = Number()
