from guerrillamail import GuerrillaMailSession
import re, csv

class Silverback(object):

    def __init__(self, addr):
        self.session = GuerrillaMailSession(email_address=addr)

    def print_body(self, offset=0):
        print(self.session.get_email(self.session.get_email_list()[offset].guid).body)

    def get_all_mail(self):
        mails = []
        for g in self.session.get_email_list():
            mails.append(self.session.get_email(g.guid))
        return mails

    def clean_text(self, rgx_list, text):
        new_text = text
        for rgx_match in rgx_list:
            new_text = re.sub(rgx_match, '', new_text)
        return new_text

    def search_and_write(self):
        mails = self.get_all_mail()
        counter = 0
        pattern = "([\w]+[\w\s]*)(?=[\'""\s]*<{1})"
        with open('./data.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for item in mails:
                f = item.sender
                s = item.subject
                j = self.clean_text(["<.*>", "\n", "\t"], item.body)

                if s and f and j:
                    writer.writerow([f, s, j])
                    counter += 3

        print("wrote %i pieces of data to csv" % counter)


if __name__ == "__main__":
    s = Silverback("john@sharklasers.com")
    s.search_and_write()
