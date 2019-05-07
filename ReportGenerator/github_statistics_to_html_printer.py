class GithubStatisticsToHtmlPrinter(object):

    @staticmethod
    def print_chart(chart_url: str) -> str:
        html = '''
            <iframe style="width:100%; height: 500px;" frameborder="0" seamless="seamless" scrolling="no" \ 
                src="''' + chart_url + '''.embed?height=500"></iframe>
        '''

        return html
