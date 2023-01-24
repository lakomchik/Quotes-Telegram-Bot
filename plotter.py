import matplotlib.pyplot as plt

class Plot:

    def draw_data(self, id, quote):
        plt.scatter(id, quote, color = 'b')
        plt.xlabel('id')
        plt.ylabel('Price')
        plt.savefig('multiple_quote.png')
