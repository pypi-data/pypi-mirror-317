import time
import re
from scrapeanything.scraper.models.element import Element
from scrapeanything.scraper.types import Types
from scrapeanything.scraper.props import Props
from scrapeanything.scraper.functions import Functions
from scrapeanything.utils.type_utils import TypeUtils

class Scraper:

    def __del__(self) -> None:
        self.on_close()

    def wget(self, url: str, tries: int=0) -> None:
        try:
            if url is not None and tries < 3:
                self.parser = self.on_wget(url)
            
        except Exception as ex:
            tries += 1
            time.sleep(3)
            self.wget(url, tries)

    def xPath(self, path: str, element: Element=None, pos: int=0, data_type: str=None, prop: str=None, explode: str=None, condition: str=None, substring: str=None, transform: str=None, replace: str=None, join: str=None, timeout: int=None, is_error: bool=True):
        if path is None or path == '':
            return None

        # step 1: get elements
        elements = self._get_elements(path=path, element=element, timeout=timeout, is_error=is_error)

        # step 2: apply properties
        results = self._apply_property(elements=elements, pos=pos, prop=prop)

        # step 3: apply functions
        results = self._apply_functions(elements=results, substring=substring, explode=explode, replace=replace, join=join)

        # # step 4: apply transform
        # if transform is not None:
        #     response = self._transform(element=response, transform=transform)

        # step 5: clean results
        # clean string if element is not of ay complex type (WebElement, any object type, ...)
        results = self._clean_elements(elements=results)

        # step 6: apply dataTypes
        results = self._apply_datatype(elements=results, data_type=data_type, condition=condition)

        # step 7: return values
        if len(results) == 1 and data_type != Types.LIST:
            results = results[0]
        elif len(results) == 0 and data_type != Types.LIST:
            results = None
        elif pos is not None:
            results = results[pos]
    
        return results
    
    def _get_elements(self, path: str, element: Element=None, timeout: int=None, is_error: bool=True) -> Element | list[Element]:
        element = self.parser if element is None else element
        return self.on_xPath(element=element, path=path, timeout=timeout, is_error=is_error)
    
    def _apply_property(self, elements: list[Element], pos: int=None, prop: str=None) -> Element:
        if prop is None:
            return elements

        results = []
        
        for item in elements:
            if prop == Props.TEXT:
                results.append(self.on_get_text(item))
            elif prop == Props.HTML:
                results.append(self.on_get_html(item))
            elif prop is not None:
                results.append(self.on_get_attribute(item, prop))
            else:
                results.append(Element(element=item))
        
        return results

    def _apply_functions(self, elements: list[Element], substring: str=None, explode: str=None, replace: str=None, join: str=None) -> list[Element] | list[str]:
        if substring is None or explode is None or replace is None or join is None:
            return elements        
        
        results = []

        options = dict(locals())
        for option in options:
            for element in elements:
                if option == Functions.SUBSTRING and substring is not None:
                    element = self.substring(element, substring)
                if (option == Functions.EXPLODE) and explode is not None:
                    element = self.explode(element, explode)
                if option == Functions.REPLACE and replace is not None:
                    element = self.replace(element, replace)
                if option == Functions.JOIN and join is not None:
                    element = self.join(element, join)
                    
                results.append(element)
                    
        return results
    
    def _apply_datatype(self, elements: list[Element] | list[str]=None, data_type: str=None, condition: str=None) -> list[Element] | list[str] | list[int] | list[float]:
        results = []
        
        if (data_type is None or data_type == Types.ELEMENT) and isinstance(elements[0], Element):
            return elements

        if data_type is not None and isinstance(elements[0], Element):
            raise Exception(message='Data Type is incompatible with extracted data')

        if data_type is not None and '[' in data_type: # in the case dataType is a datetime with format (DATE[%Y-%m-%d %H:%M:%S])
            tokens = data_type.split('[')
            data_type = tokens[0]
            format = tokens[1][:-1]

        
        for element in elements:
            if data_type == Types.DATE:
                result = TypeUtils.to_date(value=element, format=format)
            elif data_type == Types.PERCENTAGE:
                result = TypeUtils.to_number(value=element.replace('%', ''))
            elif data_type == Types.BOOL:
                result = self.eval_condition(value=element, condition=condition)
            elif data_type == Types.MONEY:
                result = TypeUtils.to_money(value=element)
            elif data_type == Types.NUMBER:
                result = TypeUtils.to_number(value=element)
            elif data_type == Types.INTEGER:
                result = TypeUtils.to_integer(value=element)
            elif data_type == Types.GEO:
                result = TypeUtils.to_geo(value=element)
            elif data_type == Types.CHAR or data_type == Types.STRING:
                result = TypeUtils.to_char(value=element)
            elif data_type == Types.URL:
                base_url = TypeUtils.to_base_web(url=self.publisher.url)
                result = TypeUtils.to_normalized_url(base_url=base_url, element=element)
            else:
                result = element

            results.append(result)

        return results

    def _clean_elements(self, elements: list[str]) -> list[str] | list[Element]:
        results = []
        
        primitive = (str) # (int, str, bool)
        if elements[0] is not None and not isinstance(elements[0], primitive):
            return elements

        for result in elements:
            if result is not None and isinstance(result, primitive):
                result = result.replace('\n', '').strip()
                results.append(result)

        return results

    def exists(self, path: str, element: Element=None, timeout: int=None, is_error: bool=False):
        return self.on_exists(path=path, element=element, timeout=timeout, is_error=is_error)

    def substring(self, el: any, substring: str):
        if substring is not None and el is not None:
            idx_separator1 = None
            idx_separator2 = None

            index = [m.start() for m in re.finditer('"', substring)][1]
            separator1 = substring[:index+1].replace('"', '', 9999).strip()
            separator2 = substring[index+2:].replace('"', '', 9999).strip()

            idx_separator1 = el.index(separator1) + len(separator1)
            idx_separator2 = el.index(separator2)

            if idx_separator1 is not None and idx_separator2 is not None:
                el = el[idx_separator1:idx_separator2]

        return el       

    def explode(self, el, explode):
        '''
        Description:
        Arguments:
        Returns:
        '''
        
        tokens = []
        separator_find = None
        separator_replace = None

        if explode is not None and el is not None:
            separators, indexes = explode.rsplit(',', 1)

            separators = separators.split(';')

            separator_find = separators[0].strip(' ').replace('"', '', 9999)
            if len(separators) > 1:
                separator_replace = separators[1].strip(' ').replace('"', '', 9999)


            for index in indexes.split(';'):
                index = int(index.strip(' '))
                if el is not None and separator_find in el:
                    el = el.split(separator_find)[index]
                else:
                    el = ''
                
                tokens.append(el)

        if separator_replace is None:
            separator_replace = ' '
        
        return separator_replace.join(tokens).strip(' ')

    def replace(self, el: any, replace: str):
        elements = []

        if replace is not None and el is not None:
            groups = replace.replace('; ', ';').split(';')
            for i, group in enumerate(groups):
                replace = group.replace(', ', ',')
                tokens = [ token.replace('"', '') for token in replace.split(',') ]
                
                el = el.replace(tokens[0], tokens[1])
                
        return el

    def join(self, el: any, separator: str):
        if type(el) is list and separator is not None and separator != '':
            el =  [ e for e in el if e is not None and e != '' ]
            return separator.join(el)
        else:
            return el

    def _transform(self, element, transform):
        return element

        if transform is not None and element is not None:
            for couple in transform:
                from_value, to_value = couple
            return element # TODO
        else:
            return element

    def eval_condition(self, element, condition):
        return eval('element ' + condition)
        '''
        try:
            return eval('int(element) ' + condition)
        except Exception as e:
            return eval('element ' + condition)
        '''

    def hover(self, path: str, element: Element=None, is_error: bool=True, timeout: int=99) -> None:
        self.on_hover(path=path, element=element, is_error=is_error, timeout=timeout)

    def enter_text(self, path: str, text: str, element: Element=None, clear: bool=False, timeout: int=None, is_error: bool=False):
        return self.on_enter_text(path=path, text=text, element=element, clear=clear, timeout=timeout, is_error=is_error)

    def click(self, path: str, element: Element=None, timeout: int=None, pos: int=0, is_error: bool=True) -> None:
        self.on_click(path=path, element=element, timeout=timeout, pos=pos, is_error=is_error)

    def click_all(self, path: str, element: Element=None, timeout: int=None, pos: int=0, is_error: bool=True) -> None:
        self.on_click_all(path=path, element=element, timeout=timeout, is_error=is_error)

    def click_and_hold(self, path: str, seconds: float, element: Element=None, timeout: int=None, is_error: bool=True) -> None:
        self.on_click_and_hold(path=path, seconds=seconds, element=element, timeout=timeout, is_error=is_error)

    def back(self):
        self.on_back()

    def get_current_url(self):
        return self.on_get_current_url()

    def solve_captcha(self, path: str):
        self.on_solve_captcha(path=path)

    def get_css(self, element: Element, prop: str) -> str:
        return self.on_get_css(element.scraper.parser, prop)

    def login(self, username_text: str=None, username: str=None, password_text: str=None, password: str=None) -> None:
        self.on_login(username_text=username_text, username=username, password_text=password_text, password=password)

    def search(self, path: str=None, text: str=None, timeout: int=99) -> None:
        return self.on_search(path=path, text=text, timeout=timeout)

    def scroll_to_bottom(self) -> None:
        return self.on_scroll_to_bottom()

    def get_scroll_top(self) -> int:
        return self.on_get_scroll_top()

    def get_scroll_bottom(self):
        return self.on_get_scroll_bottom()

    def select(self, path: str, option: str) -> None:
        self.on_select(path=path, option=option)

    def get_image_from_canvas(self, path: str, local_path: str, element: Element) -> str:
        return self.on_get_image_from_canvas(path=path, local_path=local_path, element=element)

    def switch_to(self, element: Element) -> None:
        return self.on_switch_to(element=element)

    def screenshot(self, path: str=None, file: str=None) -> None:
        return self.on_screenshot(path=path, file=file)

    def freeze(self) -> None:
        self.on_freeze()

    def unfreeze(self) -> None:
        self.on_unfreeze()
        
    def get_cookies(self) -> 'list[dict]':
        return self.on_get_cookies()

    def close(self):
        self.on_close()