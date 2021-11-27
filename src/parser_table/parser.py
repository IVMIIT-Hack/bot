from html.parser import HTMLParser 
# Пасхалка: Не изобретай велосипед, а просто улучи его!

class HTMLTableParser(HTMLParser):
    """
        Этот класс служит в качестве анализатора таблиц html. Он способен анализировать несколько
        таблицы, которые вы вводите. Вы можете получить доступ к полю результат по таблицам.
    """
    def __init__(
        self,
        decode_html_entities=False,
        data_separator=' ',
    ):

        HTMLParser.__init__(self, convert_charrefs = decode_html_entities)

        self._data_separator = data_separator

        #Дефолтно у нас ничего нет пока что.
        self._in_td = False
        self._in_th = False
        self._current_table = []
        self._current_row = []
        self._current_cell = []
        self.tables = []

    def handle_starttag(self, tag, attrs):
        """
            Нам нужно запомнить начальную точку для интересующего содержания.
            Другие теги (<table>, <tr>) обрабатываются только в момент закрытия для недопущения дублирования и выхода за предел.
        """
        if tag == 'td':
            self._in_td = True
        if tag == 'th':
            self._in_th = True

    def handle_data(self, data):
        """
            Здесь мы сохраняем содержимое в ячейку.....
        """
        if self._in_td or self._in_th:
            self._current_cell.append(data.strip())
    
    def handle_endtag(self, tag):
        """
            Здесь мы выходим из тегов. Если закрывающий тег </tr>, мы знаем, что мы можно сохранить
            наши анализируемые в данный момент ячейки в текущую таблицу в виде строки и подготовиться к новой строке. 
            Если закрывающий тег </table>, мы сохраняем текущую таблицу и готовимся к новой.
        """
        if tag == 'td':
            self._in_td = False
        elif tag == 'th':
            self._in_th = False

        if tag in ['td', 'th']:
            final_cell = self._data_separator.join(self._current_cell).strip()
            self._current_row.append(final_cell)
            self._current_cell = []
        elif tag == 'tr':
            self._current_table.append(self._current_row)
            self._current_row = []
        elif tag == 'table':
            self.tables.append(self._current_table)
            self._current_table = []