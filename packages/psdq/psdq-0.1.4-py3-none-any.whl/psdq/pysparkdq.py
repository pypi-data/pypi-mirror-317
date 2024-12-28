from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import functools
import re

class PySparkDQ:
  def __init__(self, spark_session:SparkSession, df:SparkDataFrame, warning_rows=1_000_000, use_logging=False, log_level='WARNING'):
    """
    spark_session : SparkSession
        Spark session to be used
    df : SparkDataFrame
        Spark Dataframe to evaluate
    warning_rows (optional): float
        Class will display a warning log if class has more than this amount of rows.
    use_logging (optional): boolean
        Whether to use logging library of print statements. Defaults to False.
    log_level (optional): string
        Set the class log level. Defaults to WARNING. Can be changed after initialization with set_log_level() method.
    """
    self._spark_session = spark_session
    self._use_logging = use_logging
    self._log_level = log_level
    self._warning_rows = warning_rows
    self._df = df
    self._df_count = None
    self._result_schema = 'colname:string,test:string,scope:string,found:int,total:int,percentage:double,tolerance:double,over_under_tolerance:string,inclusive_exclusive:string,pass:boolean'
    self._log_levels=['INFO', 'WARNING', 'ERROR', 'DEBUG', 'CRITICAL'] # the order matters. Less critical -> more critical
    self._log_levels_to_display = self._log_levels[(self._log_levels.index(self._log_level)):].copy() # Class will display log levels from this list
    self._df_test_results = self._spark_session.createDataFrame([], self._result_schema)
    self._data_tests = []
    self._begin_flag=False

    assert self._log_level in self._log_levels, f"Unrecognized log_level. Possible values are {self._log_levels}"

    if self._use_logging:
      import logging

  class DataTest:
      def __init__(self, colname, test, scope, partial, tolerance=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
            assert tolerance >= 0.0 and tolerance <= 1.0, f"tolerance must be between 0.0 and 1.0 inclusive. Current value is {tolerance}"
            assert over_under_tolerance in ['over','under'], f"over_under_tolerance not in ['over','under']. Current value is {over_under_tolerance}"
            assert inclusive_exclusive in ['inclusive', 'exclusive'], f"inclusive_exclusive must be in ['inclusive', 'exclusive']. Current value is {inclusive_exclusive}"
            self._colname = colname
            self._test = test
            self._scope = str(scope)
            self._partial = partial
            self._tolerance = float(tolerance)
            self._over_under_tolerance = over_under_tolerance
            self._inclusive_exclusive = inclusive_exclusive

      def get_pyspark_row_struct(self):
            return f.struct(f.lit(self.colname).alias('colname'),
                            f.lit(self.test).alias('test'),
                            f.lit(self.scope).alias('scope'),
                            self.partial.alias('pass'),
                            )
      def __eq__(self, other: object) -> bool:
            return (
                self.colname == other.colname and
                self.test == other.test and
                self.scope == other.scope and
                str(self.partial) == str(other.partial) and
                self.tolerance == other.tolerance and
                self.over_under_tolerance == other.over_under_tolerance and
                self.inclusive_exclusive == other.inclusive_exclusive
            )
      
      @property
      def colname(self):
          return self._colname
      @property
      def test(self):
          return self._test
      @property
      def scope(self):
          return self._scope
      @property
      def partial(self):
          return self._partial
      @property
      def reverse_partial(self):
          return self._reverse_partial
      @property
      def tolerance(self):
          return self._tolerance
      @property
      def over_under_tolerance(self):
          return self._over_under_tolerance
      @property
      def inclusive_exclusive(self):
          return self._inclusive_exclusive
      
  ## ---------------- Native dq evaluations --------------------- ##

  def values_in_list(self, colname:str, val_list:list, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values in list, same as c.isIn(val_list). Defaults to all values must satisfy the condition inclusive on tolerance. 
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    val_list : list(any)
        List of values to check. Must match column datatype. 
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_in_list(colname="my_col",
    |                      value_list=[1,2,3,4],
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_in_list"
    scope = val_list
    partial = f.col(colname).isin(val_list)
    
    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_not_in_list(self, colname:str, val_list:list, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values not in list, same as ~c.isIn(val_list). Defaults to all values must satisfy the condition inclusive on tolerance. 
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value_list : list(any)
        List of values to check. Must match column datatype. 
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_not_in_list(colname="my_col",
    |                      value_list=[1,2,3,4],
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_not_in_list"
    scope = val_list
    partial = ~f.col(colname).isin(val_list)

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self
  
  def values_null(self, colname:str, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for Null values, same as c.isNull(). Defaults to all values must satisfy the conditioninclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_null(colname="my_col",
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_null"
    scope = 'null'
    partial = f.col(colname).isNull()

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_not_null(self, colname:str, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for Not Null values, same as c.isNotNull(). Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'
  
    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_not_null(colname="my_col",
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_not_null"
    scope = 'null'
    partial = f.col(colname).isNotNull()

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_equal(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values equal to value, same as c == value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_equal(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_equal"
    scope = value
    partial = f.col(colname)==scope

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self
  
  def values_not_equal(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values equal to value, same as c == value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_not_equal(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_not_equal"
    scope = value
    partial = f.col(colname)!=scope

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_between(self, colname:str, lower_value, upper_value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values between boundaries, same as c.between(lower, upper). Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    lower_value: string, int, float, column
        Lower reference to compare
    upper_value: string, int, float, column
        Upper reference to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_between(colname="my_col",
    |                      lower_value=10,
    |                      upper_value=20,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_between"
    scope = f"{lower_value} - {upper_value}"
    partial = f.col(colname).between(lower_value,upper_value)
    
    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_greater_equal_than(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values greater equal than the reference value, same as c >= value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_lower_equal_than(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_greater_equal_than"
    scope = value
    partial = f.col(colname) >= value
    reverse_partial = f.col(colname) < value

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_lower_equal_than(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values lower equal than the reference value, same as c <= value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_lower_equal_than(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_lower_equal_than"
    scope = value
    partial = f.col(colname) <= value

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_greater_than(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values greater than the reference value, same as c <= value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_greater_than(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()
  
    Returns
    -------
    None
    """
    test = "values_greater_than"
    scope = value
    partial = f.col(colname) > value

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  def values_lower_than(self, colname:str, value, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Test column for values lower than the reference value, same as c <= value. Defaults to all values must satisfy the condition inclusive on tolerance.
    If there's a different tolerance that the default one, adjust the parameters: tolerance, over_under_tolerance, inclusive_exclusive

    Parameters
    ----------
    colname : string
        Column name to evaluate.
    value: string, int, float, column
        Reference value to compare
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_lower_than(colname="my_col",
    |                      value=10,
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    test = "values_lower_than"
    scope = value
    partial = f.col(colname) > value

    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self
  
  def values_custom_dq(self, test, partial, scope=None, tolerance:float=1.0, over_under_tolerance='over', inclusive_exclusive='inclusive'):
    """
    Adds a custom data quality check. The only requiremets for the partial argument expressions is that it's written in terms of
    pyspark columns or spark sql expressions and resolves into a boolean column

    Parameters
    ----------
    test : string
        Test name to use. 
    partial: column
        Column expression that defines the test.
    scope (optional): string
        If you want to manually add your scope to identify this test feel free to do so. Defaults to the partial used on the test.
    tolerance (optional): float
        Tolerance threshold for test evaluation. ranges from 0.0 to 1.0. Defaults to 1.0.
    over_under_tolerance (optional): string
        Evaluates threshold success checking if matching records are over or under it. Options are 'over', 'under'. Defaults to 'over'.
    inclusive_exclusive (optional): string
        Whether it should consider results inclusive or exclusive on the threshold. Options are 'inclusive', 'exclusive'. Defaults to 'inclusive'

    Examples
    -------
    |  dq = PySparkDQ(...) 
    |  dq.begin().values_custom_dq(test="My Custom Test",
    |                      partial=expr("my_date_col = '2024-12-01' and my_numeric_col between 10 and 50"),
    |                      tolerance=0.8,
    |                      over_under_tolerance='under',
    |                      inclusive_exclusive='inclusive')
    |            .evaluate()

    Returns
    -------
    None
    """
    scope = scope if scope is not None else str(partial)
    colname = "N/A"
    data_test = self.DataTest(colname, test, scope, partial, tolerance, over_under_tolerance, inclusive_exclusive)
    if self._add_test_to_queue(data_test):
        self._add_to_summary_report(data_test)
    return self

  ## ----------------------- User Main Functions ----------------------- ##

  def get_summary(self, cache_result=True) -> SparkDataFrame:
    """
    Evaluates all tests and returns a SparkDataFrame with the test summaries.

    Parameters
    ----------
    cache_result (optional): boolean
        Option to cache the result or not. Defaults to True.

    Examples
    -------
    |  dq = PySparkDQ(...)
    |  
    |  df_summary=dq.begin().values_custom_dq(test="My Custom Test 2",
    |  partial=( (col('my_float_col') >= 250.9) & (col('my_bool_col') == False))
    |  .get_summary()

    Returns
    -------
    SparkDataFrame
    """
    self._calculate_test_results()

    if cache_result:
        self._df_test_results = self._df_test_results.cache()
    self._begin_flag=False
    
    return self._df_test_results

  def get_row_level_qa(self) -> SparkDataFrame:
    """
    Evaluates all tests row-by-row and returns the initial dataframe with extra columns for test results.

    Parameters
    ----------
    None

    Examples
    -------
    |  dq = PySparkDQ(...)
    |  dq.begin().custom_dq(test="My Custom Test",
    |                      partial=expr("my_date_col = '2024-12-01 and my_numeric_col between 10 and 50")
    |                      tolerance=0.8,
    |                      over_under_tolerance='under'
    |                      inclusive_exclusive='inclusive') \
    |            .custom_dq(test="My Custom Test 2", 
    |                      partial=( (col('my_float_col') >= 250.9) & (col('my_bool_col') == False)
    |                      )
    |            .get_row_level_qa()

    Returns
    -------
    SparkDataFrame
    """
    assert len(self._data_tests) > 0, "No tests to run. Make sure to add qa tests before calling this function."
    self._df_row_level_qa = self._df.withColumn(f"pysparkdq", f.array([x.get_pyspark_row_struct() for x in self._data_tests]))\
                .withColumn('pysparkdq_fail_count', f.size(
                    f.filter('pysparkdq', lambda x: x.getField('pass')==False))) \
                .withColumn('pysparkdq_failed_tests', f.transform(
                    f.filter('pysparkdq', lambda x: x.getField('pass')==False), 
                    lambda y: y.dropFields('pass')
                )).drop('pysparkdq')
    return self._df_row_level_qa
      
  def evaluate(self) -> None:
    """
    Evaluates the test summary and throws an exception if anything fails.

    Parameters
    ----------
    None

    Examples
    -------
    |  dq = PySparkDQ(...)
    |  dq.begin().custom_dq(test="My Custom Test",
    |                      partial=expr("my_date_col = '2024-12-01 and my_numeric_col between 10 and 50")
    |                      tolerance=0.8,
    |                      over_under_tolerance='under'
    |                      inclusive_exclusive='inclusive') \
    |            .custom_dq(test="My Custom Test 2", 
    |                      partial=( (col('my_float_col') >= 250.9) & (col('my_bool_col') == False)
    |                      )
    |            .evaluate()

    Returns
    -------
    SparkDataFrame
    """
    self._calculate_test_results()
    if self._df_test_results.isEmpty():
        self._log_message("No test summary found. Make sure to run X function to generate the summary",'INFO')
        return
    elif not self._df_test_results.filter('pass = false').isEmpty():
        failed_tests=self._df_test_results.filter('pass = false')
        cnt = failed_tests.count()
        which = [{'colname': x['colname'], 'test': x['test'], 'scope': x['scope']} for x in failed_tests.select('colname','test','scope').collect()]
        assert self._df_test_results.filter('pass = false').isEmpty(), f"Detected failed tests. Count: {cnt}, Tests: {which}"
    else:
        self._log_message("All tests passed", 'INFO')

  ## ------------------------------ User Auxiliary functions --------------------- ##

  def set_log_level(self, log_level):
    f"""
    Change the log level of this object after initialization.

    Parameters
    ----------
    log_level : string
      Possible log levels are {self._log_levels}
    -------
    None
    """
    assert log_level in self._log_levels, f"log_level not in {self._log_levels}"
    self._log_levels_to_display = self._log_levels[(self._log_levels.index(self._log_level)):].copy() # Class will log levels on this list

  ## ------------------------------ Internal functions ---------------------- ##

  def _calculate_test_results(self) -> None:
    self._count_records() # As this function depends on total record count we have to add this at the beginning.
    
    percentage_tolerance = f.when(f.col('over_under_tolerance') == 'over', 
                                    f.when(f.col('inclusive_exclusive') == 'inclusive', f.col('percentage')>=f.col('tolerance')).otherwise(f.col('percentage')>f.col('tolerance'))
                                  ).otherwise(
                                     f.when(f.col('inclusive_exclusive') == 'inclusive', f.col('percentage')<=f.lit(f.col('tolerance'))).otherwise(f.col('percentage')<f.lit(f.col('tolerance')))
                                  )
    
    self._df_test_results = self._df_test_results.withColumn('total', f.when(f.col('total').isNull(),f.lit(self._df_count)).otherwise(f.col('total')))\
                            .withColumn('percentage', f.round(f.col('found')/f.lit(self._df_count),8).alias('percentage')) \
                            .withColumn('pass',percentage_tolerance)

  def _count_records(self):
    if self._df_count == None:
      self._log_message(message="Counting total records for evaluation...", level="INFO")
      self._df_count = self._df.count()

    if self._df_count > self._warning_rows:
      self._log_message(message=f"Large number of rows detected ({self._df_count}), be aware that large datasets will take longer to compute. Consider sampling the dataframe before initializing this class", level='WARNING')

  def _add_test_to_queue(self, data_test) -> bool:
    if data_test not in self._data_tests:
        over_under_str = 'at least' if data_test.over_under_tolerance == 'over' else 'up until'
        self._log_message(message=f"Checking {data_test.test} for {data_test.colname} - {over_under_str} {round(100*data_test.tolerance,4)}% of total rows", level='INFO')
        self._data_tests.append(data_test)
        return True
    else:
       return False
                                  
  def _add_to_summary_report(self, data_test:DataTest):
    # Setting summary report row for this test
    self._df_test_results = self._df_test_results.unionByName(
                            self._df.filter(data_test.partial).select(
                            f.lit(data_test.colname).alias('colname'),
                            f.lit(data_test.test).alias('test'),
                            f.lit(data_test.scope).alias('scope'),
                            f.sum(f.when(data_test.partial,1).otherwise(0)).alias("found"),
                            f.lit(self._df_count).alias("total"),
                            f.round(f.col('found')/f.lit(self._df_count),8).alias('percentage'),
                            f.lit(data_test.tolerance).alias('tolerance'),
                            f.lit(data_test.over_under_tolerance).alias('over_under_tolerance'),
                            f.lit(data_test.inclusive_exclusive).alias('inclusive_exclusive'),
                            f.lit(None).alias("pass")
                            ))
      
  def _log_message(self, message:str, level:str):
    if level in self._log_levels_to_display:
      if self._use_logging:
          if self._log_level=="INFO": 
              self._logging.info(message)
          elif self._log_level=="WARNING": 
              self._logging.warning(message)
          elif self._log_level=="ERROR":
              self._logging.error(message)
          elif self._log_level=="DEBUG":
              self._logging.debug(message)
          elif self._log_level=="CRITICAL":
              self._logging.critical(message)
      else:
          if level in self._log_levels_to_display: 
              print(f"[{level}] {message}")
  
  def __repr__(self):
    return str()
  
  def __str__(self):
    return f"Spark Data Quality Tool - Checks for enhanced data quality !"