class card_parser:
    def card(string):
        if string == '050001fbf23d':
            return ''
        string = string[10:-4]
        return string

    def cards(string, data):
        if string == '050001fbf23d':
            return []
        finding_cards = []
        lenght = int(string[8:10])
        string = string[10:]
        string = string[:-4]
        for i in range(lenght):
            for j in range(len(data)): 
                index = string.find(str(data[j]))
                if index != -1:
                    finding_cards.append(string[index:(index+len(str(data[j])))])
                    string = string[:index] + string[(index+len(str(data[j]))):]
                    break
        return finding_cards            
