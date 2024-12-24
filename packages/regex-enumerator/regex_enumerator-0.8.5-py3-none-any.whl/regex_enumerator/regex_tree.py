class RegexTree:
    pass


class CharClasses:
    def __init__(self, chars_list: list[str], min_len: int, max_len: int):
        self._index = 0
        self._chars: str = ''.join(sorted(set(''.join(chars_list))))
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._chars)
        self.done = self._base == 0 or self._max_len == 0
        self._max_index = self._calculate_max_index()
        if self._base >= 1:
            self._start = self._base ** max(self._min_len, 1)
        if self.done:
            self.current: list[str] = ['']
            return

        self.current = [self._calculate()]
        if self._min_len == 0:
            self.current.append('')

    def _calculate_max_index(self) -> int | None:
        if self._max_len is None or self.done:
            return None
        if self._base == 1:
            return self._max_len - self._min_len
        return ((self._base ** max(self._min_len, 1) - self._base ** (self._max_len + 1)) // (1 - self._base)) - 1

    def _calculate(self) -> str:
        if self._max_len is not None and self._index >= self._max_index:
            self.done = True

        if self._base == 1:
            return self._chars[0] * (self._min_len + self._index)

        result = []
        num = self._start + self._index
        while num > 1:
            result.append(self._chars[num % self._base])
            num //= self._base

        return ''.join(reversed(result))

    def next(self) -> set[str]:
        assert not self.done

        self._index += 1
        new_value = self._calculate()
        assert new_value not in self.current
        self.current.append(new_value)
        return [new_value]


class BackReference:
    def __init__(self, reference: RegexTree, min_len: int, max_len: int | None):
        self._min_len = min_len
        self._max_len = max_len
        self._index = 0
        self.reference: RegexTree = reference
        self.done = max_len == 0 or (
            reference.done and len(reference.current) == 0)
        self.current: dict[str, list[str]
                           ] = self._calculate() if not self.done else {}

    def update(self):
        if self._max_len is not None and self._min_len + self._index >= self._max_len and self.reference.done:
            self.done = True

        for string in self.reference.current:
            if string in self.current:
                self.current[string].append(
                    string * (self._min_len + self._index))
            else:
                self.current[string] = []
                for i in range(self._min_len, self._min_len + self._index + 1):
                    self.current[string].append(string * i)

    def _calculate(self) -> dict[str, set[str]]:
        current_ref = self.reference.current
        if self._max_len is not None and self._min_len + self._index >= self._max_len:
            self.done = True

        result: dict[str, list[str]] = {}

        for string in current_ref:
            result[string] = [string * (self._min_len + self._index)]

        return result

    def next(self) -> dict[str, set[str]]:
        assert not self.done
        self._index += 1
        if self._max_len is not None and self._min_len + self._index >= self._max_len:
            self.done = True

        for string in self.current.keys():
            self.current[string].append(string * (self._min_len + self._index))

        return self.current


class Alternative:
    def __init__(self, elements: list[CharClasses | RegexTree | BackReference]):
        self._index = 0
        self._elements: list[CharClasses | RegexTree | BackReference] = [
            element for element in elements if not element.done or len(element.current) > 0]
        self._base = len(self._elements)
        self.done = self._base == 0
        self.current: set[str] = self._calculate() if not self.done else {''}

    def next(self) -> set[str]:
        assert not self.done
        assert not isinstance(self._elements[0], BackReference)

        index = self._index + 1
        if index >= self._base:
            index = 0
        while self._elements[index].done:
            index += 1
            if index >= self._base:
                index = 0

        self._index = index
        result: list[tuple[str, dict[RegexTree, str]]] = []

        if isinstance(self._elements[0], CharClasses):
            for string in self._elements[0].next() if index == 0 else self._elements[0].current:
                result.append((string, {}))
        else:
            for string in self._elements[0].next() if index == 0 else self._elements[0].current:
                result.append((string, {self._elements[0]: string}))

        done = self._elements[0].done

        for i, element in enumerate(self._elements[1:], start=1):
            temp = []
            if isinstance(element, CharClasses):
                for sfx in element.next() if i == index else element.current:
                    for pfx in result:
                        temp.append((pfx[0] + sfx, pfx[1]))
            elif isinstance(element, RegexTree):
                for sfx in element.next() if i == index else element.current:
                    for pfx in result:
                        temp.append((pfx[0] + sfx, {**pfx[1], element: sfx}))
            else:
                if i == index:
                    element.next()
                for pfx in result:
                    reference = pfx[1][element.reference]
                    assert reference is not None
                    for sfx in element.current[reference]:
                        temp.append(
                            (pfx[0] + sfx, pfx[1]))
            result = temp
            done = done and element.done

        self.done = done
        new_strings = {struct[0] for struct in result} - self.current
        self.current.update(new_strings)
        return new_strings

    def _calculate(self) -> set[str]:
        assert not isinstance(self._elements[0], BackReference)

        result: list[tuple[str, dict[RegexTree, str]]] = []

        if isinstance(self._elements[0], CharClasses):
            for char in self._elements[0].current:
                result.append((char, {}))
        else:
            for char in self._elements[0].current:
                result.append((char, {self._elements[0]: char}))

        done = self._elements[0].done

        for element in self._elements[1:]:
            temp: list[tuple[str, dict[RegexTree, str]]] = []
            done = done and element.done
            if isinstance(element, CharClasses):
                for pfx in result:
                    for sfx in element.current:
                        temp.append((pfx[0] + sfx, pfx[1]))
            elif isinstance(element, RegexTree):
                for pfx in result:
                    for sfx in element.current:
                        temp.append((pfx[0] + sfx, {**pfx[1], element: sfx}))
            else:
                for pfx in result:
                    reference = pfx[1][element.reference]
                    assert reference is not None
                    for sfx in element.current[reference]:
                        temp.append(
                            (pfx[0] + sfx, pfx[1]))
            result = temp

        self.done = done
        return {struct[0] for struct in result}


class RegexTree:
    def __init__(self, alternatives: list[Alternative], min_len: int, max_len: int | None):
        self.references: list[BackReference] = []
        self._alternatives: list[Alternative] = [
            alternative for alternative in alternatives if not alternative.done or len(alternative.current) > 0]
        self._min_len = min_len
        self._max_len = max_len
        self._base = len(self._alternatives)
        self.done = self._base == 0 or self._max_len == 0
        self._gen_charset = False
        self._index_charset = 0
        self._index_repetition = 0
        self._done_repetition = False
        self._current_chars: set[str] = self._calculate_chars()
        self.current: set[str] = self._calculate() if not self.done else set()

    def add_reference(self, reference: BackReference):
        if reference.done and len(reference.current) == 0:
            return
        self.references.append(reference)

    def _calculate_using_new_charset(self) -> set[str]:
        assert not self.done
        assert self._index_repetition + self._min_len != 0
        if self._done_repetition and self._done_charset:
            self.done = True

        result = set()
        for i in range(self._min_len + self._index_repetition):
            temp = set(self._current_chars)
            for _ in range(i):
                temp.update(
                    {pfx + sfx for pfx in temp for sfx in self._current_chars})
            result.update(temp)

        return result

    def next(self) -> set[str]:
        assert not self.done

        if self._done_charset:
            self._gen_charset = False
        elif self._done_repetition:
            self._gen_charset = True

        if self._gen_charset:
            _: set[str] = self._next_charset()
            # Optimization: use the new charset to calculate the next set of strings
            result: set[str] = self._calculate_using_new_charset()
        else:
            if not self._done_repetition:
                self._index_repetition += 1
            result: set[str] = self._calculate()

        self._gen_charset = not self._gen_charset
        result -= self.current
        if len(result) == 0:
            return result

        self.current.update(result)
        if len(self.references) == 0:
            return result

        for reference in self.references:
            reference.update()
        return self.current

    def _calculate(self) -> set[str]:
        if self._max_len is not None and self._index_repetition + self._min_len >= self._max_len:
            self._done_repetition = True
            if self._done_charset:
                self.done = True

        if self._index_repetition + self._min_len == 0:
            return {''}

        result = set(self._current_chars)
        for _ in range(1, self._min_len + self._index_repetition):
            result = {pfx + sfx for pfx in result for sfx in self._current_chars}

        return result

    def _next_charset(self) -> set[str]:
        assert not self._done_charset

        index_charset = self._index_charset + 1
        if index_charset >= self._base:
            index_charset = 0
        while self._alternatives[index_charset].done:
            index_charset += 1
            if index_charset >= self._base:
                index_charset = 0

        self._index_charset = index_charset
        new_chars = self._alternatives[index_charset].next()
        self._done_charset = all(alt.done for alt in self._alternatives)
        new_chars -= self._current_chars
        self._current_chars.update(new_chars)
        return new_chars

    def _calculate_chars(self) -> set[str]:
        result = set()
        done_charset = True

        for alternative in self._alternatives:
            result.update(alternative.current)
            done_charset = done_charset and alternative.done

        self._done_charset = done_charset
        return result
