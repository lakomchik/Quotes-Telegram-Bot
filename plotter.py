import matplotlib.pyplot as plt
import os


class Plot:
    def draw_data(self, block_number_list, quotes):

        fig, ax = plt.subplots(figsize=(12, 6))
        plt.tick_params(labelsize=15)
        ax.plot(block_number_list, quotes, linewidth=4)
        ax.set_xlabel("Block number", fontsize=20)
        ax.set_ylabel("Quote", fontsize=20)
        ax.legend(fontsize=20)

        plt.savefig("quote_plot.png")

    def draw_alert(self, block_number_list, quotes, entry_price, alert_price):

        fig, ax = plt.subplots(figsize=(12, 6))
        plt.tick_params(labelsize=15)
        ax.plot(block_number_list, quotes, linewidth=4)
        ax.set_xlabel("Block number", fontsize=20)
        ax.set_ylabel("Quote", fontsize=20)

        plt.axhline(y=entry_price, color="g", linestyle="-", label="Entry price")
        plt.axhline(y=alert_price, color="r", linestyle="-", label="Alert price")
        plt.legend(fontsize=12)

        plt.savefig("quote_plot.png")

    def delete_picture(self):

        myfile = "quote_plot.png"
        if os.path.isfile(myfile):
            os.remove(myfile)
