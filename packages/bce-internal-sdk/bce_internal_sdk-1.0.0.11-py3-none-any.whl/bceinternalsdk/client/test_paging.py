# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
import unittest
from paging import PagingRequest


class TestPaging(unittest.TestCase):
    """
    Test paging
    """

    def test_paging(self):
        """
        Test paging
        """

        req = PagingRequest(
            pageNo=1,
            pageSize=10,
            orderBy="create_time",
            order="desc")
        print(req.model_dump(by_alias=True))
        self.assertEqual(req.orderby, "create_time")
        self.assertEqual(req.order, "desc")
        print(req.get_page_no())
        print(req.get_page_size())


if __name__ == '__main__':
    unittest.main()
