class CLI:
    def spacy_train(self, config, output_to, train_data, dev_data):
        cmd = \
            f"python -m spacy train '{config}' --output '{output_to}' --paths.train '{train_data}' --paths.dev '{dev_data}'"
        self.run(cmd)

    def run(self, cmd):
        import subprocess
        subprocess.run(["powershell", cmd], shell=True)
