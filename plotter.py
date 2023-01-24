import matplotlib.pyplot as plt
import os


class Plot:
    def draw_data(self, block_number_list, quotes, entry_price=0, alert_price=0):
        plt.style.use("dark_background")
        block_number_list = list(map(str, block_number_list))
        fig, ax = plt.subplots(figsize=(12, 7))
        fig.autofmt_xdate(rotation=45)
        plt.tick_params(labelsize=15)
        ax.plot(block_number_list, quotes, linewidth=6)
        ax.xaxis.set_major_locator(plt.MaxNLocator(6))
        ax.yaxis.set_major_locator(plt.MaxNLocator(7))
        ax.set_xlabel("Block number", fontsize=20)
        ax.set_ylabel("Quote", fontsize=20)
        if entry_price != 0 and alert_price != 0:
            plt.axhline(
                y=entry_price,
                color="g",
                linewidth=6,
                linestyle="-",
                label="Entry price",
            )
            plt.axhline(
                y=alert_price,
                color="r",
                linewidth=6,
                linestyle="-",
                label="Alert price",
            )
        plt.legend(fontsize=12)
        # ax.legend(fontsize=20)
        plt.savefig("quote_plot.png")

    def delete_picture(self):

        myfile = "quote_plot.png"
        if os.path.isfile(myfile):
            os.remove(myfile)
