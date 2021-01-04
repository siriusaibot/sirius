from transformers import AutoModelWithLMHead, AutoTokenizer
import torch
import os


class BertForIntent():
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")  # gpu
            print("Using that sweet " + torch.cuda.get_device_name(self.device) + "!!!")
        else:
            self.device = torch.device("cpu")    # cpu
            print("No gpu found!")

        self.tokenizer = AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased")
        self.model = AutoModelWithLMHead.from_pretrained(
            "HooshvareLab/bert-fa-base-uncased").to(self.device)

    def __call__(self, question):
        sequence = "«" + question + "» درمورد [MASK] است."

        input = self.tokenizer.encode(sequence, return_tensors="pt").to(self.device)
        mask_token_index = torch.where(input == self.tokenizer.mask_token_id)[1]

        token_logits = self.model(input).logits
        return token_logits[0, mask_token_index, :]


class IntentClassifier(torch.nn.Module):
    def __init__(self, big=False, checkpoint="./acc_84-140_checkpoint.pt"):
        super(IntentClassifier, self).__init__()

        self.big = big
        if big:
            self.hid1 = torch.nn.Linear(100000, 200)
            self.oupt = torch.nn.Linear(200, 5)
        else:
            self.oupt = torch.nn.Linear(100000, 5)

        self.Bert = BertForIntent()

        if checkpoint:
            self.load_state_dict(torch.load(checkpoint, map_location=self.Bert.device))

        self.to(self.Bert.device)

    def forward(self, x):
        if self.big:
            x = torch.tanh(self.hid1(x*1E-4))
        x = self.oupt(x)
        return x

    def classify(self, question):
        out = self.Bert(question)
        with torch.no_grad():
            intent = torch.argmax(self(out))
            if not intent:
                intent = -1
            return int(intent)


if __name__ == "__main__":
    intent_model = IntentClassifier()
