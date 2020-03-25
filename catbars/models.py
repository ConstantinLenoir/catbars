import math
from collections import Counter
from abc import ABC, abstractmethod
import pprint
import logging



class ModelFactory:
    def __init__(self,
                 numbers,
                 **kwargs):
        
        global_view = kwargs['global_view']
        del kwargs['global_view']
        
        if global_view is True:
            self.model = GlobalViewModel(numbers,
                                         **kwargs)
        else:
            self.model = BasicModel(numbers,
                                    **kwargs)
        
        self.model.build()


class AbstractModel(ABC):

    def __init__(self,
                 numbers,
                 left_labels = None,
                 right_labels = None,
                 colors = None,
                 sort = False,
                 slice = None,
                 default_label = 'else',
                 color_dic = None,
                 default_color = 'black',
                 tints = []):


        
        # There are four possible features.
        # Only "numbers" is mandatory.
        self.numbers = numbers
        self.left_labels = left_labels
        self.right_labels = right_labels
        self.colors = colors
        
        # The following three attributes work together.
        # 0, 1, 2 and 3 are both indices and implicit identifiers.
        self._features = ['numbers',
                          'left_labels',
                          'right_labels',
                          'colors'] # Pointers.
        self._feature_indices = [None,
                                 None,
                                 None,
                                 None]
        self._actual_features = []    
        
        self._color_dic = color_dic
        self._tints = tints
        self._default_label = default_label
        self._slice = slice
        self._sort_option = sort
        self.length = None

        self.minimum = None # spread, global_view.
        self.maximum = None
        self.default_color = default_color
        self.actual_colors = None
        self.legend_colors = None
        self.legend_labels = None
        self.spread = None
        
        

        ###################################################################
        
        # Validation.
        container_names = [name for name in self._features
                           if self._is_a_container(getattr(self, name))]
        option_names = [name for name in self._features
                        if not self._is_a_container(getattr(self, name))]
        self._validate_feature_containers(container_names)
        self._validate_length(container_names)
        self.length = len(self.numbers)
        self._validate_feature_options(option_names)
        self._validate_numbers()
        self._validate_slice()
        


    @abstractmethod
    def build(self):
        pass


    def _is_a_container(self, arg):
        return (arg is not None and
                not isinstance(arg, str))


    def _validate_feature_options(self, attribute_names):
        for name in attribute_names:
            text = """
The value of "{}" is not valid. "{}" must be either an
iterable container or a str option ('rank' or 'proportion').
""".format(name, name)
            value = getattr(self, name)
            if not value in [None, 'rank', 'proportion']:
                # For "labels" and "right_labels".
                raise ValueError(text.strip())
            if name == 'colors' and value is not None:
                text = """
The value of "{}" is not valid. "{}" must be either an
iterable container.
""".format(name, name)
                raise ValueError(text.strip())


    def _validate_feature_containers(self, attribute_names):
        try:
            for name in attribute_names:
                _ = iter(getattr(self, name))
        except TypeError:
            text = """
The value of "{}" is not valid. "{}" must be either an
iterable container or an str option ('rank' or 'proportion').
""".format(name, name)
            raise TypeError(text.strip())


    def _validate_length(self, feature_names):
        n = None
        for name in feature_names:
            new_n = len(getattr(self, name))
            if n is None:
                n = new_n
            elif n != new_n:
                text = """
Feature containers have to be the same length and implement __len__.
"""
                raise Exception(text.strip())


    def _validate_numbers(self):
        i = 0
        for x in self.numbers:
            x = float(x)
            if x < 0:
                text = """
Supplied numbers have to be non-negative.
({} at the zero-based position {}). 
""".format(x, i)
                raise ValueError(text.strip())
            i += 1


    def _validate_slice(self):
        if self._slice is not None:
            try:
                _, __ = (self.numbers[self._slice[0] - 1],
                         self.numbers[self._slice[1] - 1])
            except Exception:
                raise ValueError("""The given "slice" value is not valid.""")



    def _building_routine(self):
        
        self._set_actual_features()
        
        if self._sort_option:
            self._actual_features = self._sort(
                                 self._actual_features)
            self._update_features()
            self.minimum = self.numbers[-1]
            self.maximum = self.numbers[0]
        else:
            self._update_features()
            self.minimum = min(self.numbers)
            self.maximum = max(self.numbers)
        
        
        self._set_spread([self.minimum,
                          self.maximum])

        
            
        if not self._is_a_container(self.left_labels):
            self.left_labels = self._get_automatic_labels(
                self.left_labels)
            
        if not self._is_a_container(self.right_labels):
            self.right_labels = self._get_automatic_labels(
                self.right_labels)
        
        
        
        if self.colors is not None:
            if self._color_dic is not None:
                self._set_colors(self._color_dic)
            else:
                dic = self._get_color_dic()
                self._set_colors(dic)        
        
        


    def _set_actual_features(self):
        """
        Feature containers are copied, joined and
        are ready to be sorted.
        """
        for i, feature_name in enumerate(self._features):
            feature = getattr(self, feature_name)
            if (feature is not None and 
                not isinstance(feature, str)):
                
                new_feature = list(feature) # Copying.
                self._feature_indices[i] = len(self._actual_features)
                self._actual_features.append(new_feature)



    def _update_features(self):
        for i, feature_name in enumerate(self._features):
            j = self._feature_indices[i]
            if j is not None:
                setattr(self,
                        feature_name,
                        self._actual_features[j])
    

    def _sort(self, features):
        tuples = list(zip(*features))
        sorted_tuples = sorted(tuples,
                               reverse = True)
        processed_features = [list(feature) for feature
                              in zip(*sorted_tuples)]
        return processed_features
    
    
    def _get_automatic_labels(self, option):
        """
        The otpional feature remains unchanged if its value
        is None.
        """
        labels = None
        if option == 'rank':
            labels = [str(i) for i
                      in range(1, self.length + 1)]
        elif option == 'proportion':
            # "proportion" is based on the whole dataset.
            numbers_sum =  sum(self.numbers)
            labels = [self._format_perc(x / numbers_sum)
                      for x in self.numbers]
        return labels
    
    
    def _format_perc(self, x):
        p = round(100 * x)
        if p < 1:
            return '< 1 %'
        else:
            return '{} %'.format(p)


    def _set_spread(self, numbers):
        magnitudes = []
        for x in numbers:
            if x < 1:
                magnitudes.append(0)
            else:
                magnitudes.append(math.floor(math.log10(x)) + 1)

        self.spread = max(magnitudes) - min(magnitudes)


    def _get_color_dic(self):
        counter = (Counter(self.colors))
        tints_count = len(self._tints)
        categories_count = len(counter)
        too_many_categories = (categories_count > tints_count)
        n = categories_count
        if too_many_categories:
            n = tints_count
        translator = dict()
        #
        for i, e in enumerate(counter.most_common(n)):
            (category, _) = e
            translator[category] = self._tints[i]
        return translator

    
    def _set_colors(self,
                    color_dic):

        actual_colors = []
        legend_colors = []
        legend_labels = [] 
        too_many_categories = False
        # actual_colors
        for i, category in enumerate(self.colors):
            if category in color_dic:
                c = color_dic[category]
                actual_colors.append(c)
            else:
                # Residual categories are associated
                # with self.tints[-1] by default.
                actual_colors.append(self.default_color)
                too_many_categories = True
        
        for unique_category in sorted(color_dic.keys()):
            legend_labels.append(unique_category)
            legend_colors.append(color_dic[unique_category])
        if too_many_categories:
            legend_labels.append(self._default_label)
            legend_colors.append(self.default_color)

        self.actual_colors = actual_colors
        self.legend_colors = legend_colors
        self.legend_labels = legend_labels
        

    def _cut(self):
        """
        Slicing.
        """
        start, end = self._slice
        for name in [*self._features,
                      'actual_colors']:
            feature = getattr(self, name)
            if self._is_a_container(feature):
                feature = list(feature)
                setattr(self,
                        name,
                        feature[start-1:end])
        self.length = len(self.numbers)


    def _reverse(self):
        """
        The data is adapted to Matplotlib.
        """
        for feature_name in [*self._features,
                             'actual_colors']:
            feature = getattr(self,
                              feature_name)
            if self._is_a_container(feature):
                reversed_feature = list(reversed(feature))
                setattr(self,
                        feature_name,
                        reversed_feature)


    def __str__(self):
        # SEE ALSO __repr__
        # import inspect
        # members = inspect.getmembers(self)
        return pprint.pformat(self.__dict__)




class GlobalViewModel(AbstractModel):
    
    def build(self):
        
        self._building_routine()
        
        if self._slice is not None:
            self._cut()

        self._reverse()



class BasicModel(AbstractModel):
    
    def build(self):
        
        if self._slice is not None:
            self._cut()
        
        self._building_routine()
        
        
        self._reverse()


