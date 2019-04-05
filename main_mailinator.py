from pymailinator import wrapper
import html2text
import re, csv, random, datetime, os

class Mailman(object):

    api_key = "723e0d4493234625b1cb59ca6dea2e1f"
    full_path = os.path.realpath(__file__)
    directory = os.path.dirname(full_path)
    data_folder = directory + "//mailinator_data"
    list_of_names_file = directory + "/words.txt"


    def __init__(self, addr = "john", random_name = False):
        self.addr = ""
        self.inbox = wrapper.Inbox(self.api_key)
        if not random_name:
            self.addr = addr
        else:
            self.addr = self.get_random_name()

    def get_random_name(self):
        random_noun = random.choice(open(self.list_of_names_file).readlines())[0:-1]
        return random_noun

    def get_all_mail(self):
        return self.inbox.get(self.addr)

    def clean_text(self, rgx_list, text):
        new_text = text
        new_text = html2text.html2text(new_text)
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
        name_of_writing_file = self.get_current_file()
        with open(name_of_writing_file, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            for item in mails:
                f = item.fromfull.encode()
                s = item.subject.encode()
                item.get_message()
                j = self.clean_text(["<(.*?)>", "(\r\n|\r|\n)"], item.body)

                if s and f and j:
                    writer.writerow([f, s, j])
                    counter += 3

        print("wrote %i pieces of data to csv" % counter)

if __name__ == "__main__":
    m = Mailman(random_name=True)
    m.search_and_write()
    print(m.addr)




