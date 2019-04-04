from guerrillamail import GuerrillaMailSession
import re, csv, random, datetime, os

class Silverback(object):

    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)
    data_folder = directory + "//guerrilla_data"
    list_of_names_file = directory + "/nounlist.txt"


    def __init__(self, addr = "john@sharklasers.com", random_name = False):
        if not random_name:
            self.session = GuerrillaMailSession(email_address=addr)
        else:
            r_addr = self.get_random_name()
            print(r_addr)
            self.session = GuerrillaMailSession(email_address=r_addr)

    def get_random_name(self):
        random_noun = random.choice(open(self.list_of_names_file).readlines())[0:-1]
        return random_noun + "@sharklasers.com"


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
            new_text = re.sub(rgx_match, ' ', new_text)
        return new_text

    def get_current_file(self):
        n = datetime.datetime.now()
        d = str(n.month) + "-" + str(n.day) + "-" + str(n.year)
        return self.data_folder + r"/" + d + ".csv"

    def search_and_write(self):
        mails = self.get_all_mail()
        counter = 0
        pattern = "([\w]+[\w\s]*)(?=[\'""\s]*<{1})"
        name_of_writing_file = self.get_current_file()
        with open(name_of_writing_file, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for item in mails:
                f = item.sender
                s = item.subject
                j = self.clean_text(["<(.*?)>", "(\r\n|\r|\n)"], item.body)

                if s and f and j:
                    if not f == "no-reply@guerrillamail.com":
                        writer.writerow([f, s, j])
                        counter += 3

        print("wrote %i pieces of data to csv" % counter)


if __name__ == "__main__":
    s = Silverback(random_name = True)
    s.search_and_write()
