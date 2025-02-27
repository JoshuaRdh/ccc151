from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QFrame,
    QLabel,
    )
from PyQt6.QtCore import Qt, QTimer
import math
import csv
from algo import Query
from algo.getPage import getPage
from components.Details import Details
from components.PageNav import PageNav
# import gc
# import traceback

class Lists(QWidget):
    def __init__(self, data, dependencyPanel = None, dependencyPanel2 = None):
        super().__init__()
        self.data = data
        self.frame = QFrame()
        self.rows = 5
        # self.resizeDynamically(self.height())
        self.init_Query = {
            'fetchedList' : self.getList(),
            'filter_Params' : None,
            'searchedBy' : 'everywhere',
            'keyword' : '',
            'sort' : 'recent'
        }
        self.focusedIndex = 1

        self.dependencyPanel = dependencyPanel
        self.dependencyPanel2 = dependencyPanel2

        if (self.data == "students") :
            self.textColor = "#144272"
        elif (self.data == "programs") :
            self.textColor = "#a1413f"
        elif (self.data == "colleges") :
            self.textColor = "#477a72"

        self.frame.setStyleSheet(f"""
                                 QFrame{{
                                    padding: 12px;
                                    background-color: white;
                                 }}
                                 QFrame > *{{
                                    background-color: white;
                                 }}

                                 QFrame > QWidget, QPushButton {{
                                    padding: 0px;
                                    color:{self.textColor};
                                 }}       
                                 
                                 """)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.frame)

        self.myList = QVBoxLayout()
        self.myList.setContentsMargins(0,0,0,0)
        self.myList.setSpacing(0)
        self.myLists_Layout = QVBoxLayout()
        self.myLists_Layout.setContentsMargins(10,0,10,0)
        self.myLists_Layout.setSpacing(0)
        self.frame.setLayout(self.myList)

        self.queriedArr = list(reversed(self.getList())) # init 

        self.currentLastPage = math.ceil(len(self.queriedArr)/self.rows)
        self.pageNav = PageNav(self.currentLastPage, self.renderPage, self.data)
        
        self.totalCount = len(self.init_Query['fetchedList'])
        self.countLabel = QLabel(f"Total {self.data[0:1].upper()}{self.data[1:]} : {self.totalCount}")
        self.countLabel.setStyleSheet("margin-left: 3px; margin-bottom: 5px; font-weight: 550")

        self.myList.addWidget(self.countLabel)
        self.myList.addLayout(self.myLists_Layout)
        self.myList.addStretch()
        self.myList.addWidget(self.pageNav, alignment=Qt.AlignmentFlag.AlignCenter)

        paginatedArr = getPage(self.queriedArr, self.pageNav.currentPage, self.rows)
        self.renderList(paginatedArr)
        self.setLayout(main_layout)


    def renderPage(self) :
        paginatedArr = getPage(self.queriedArr, self.pageNav.currentPage, self.rows)
        self.clear_layout(self.myLists_Layout)
        self.renderList(paginatedArr)

    def renderList(self, list) :
        addHeader = True
        if len(list) == 0 :
            label = "Nothing yet..." if self.totalCount == 0 else "No Results..."
            nothing = QLabel(label)
            nothing.setStyleSheet("margin-left: 3px")
            self.myLists_Layout.addWidget(nothing)
        for index, obj in enumerate(list):
            if (addHeader) :
                self.myLists_Layout.addWidget(Details(obj))
                addHeader = False
            number = (self.pageNav.currentPage - 1) * self.rows + index + 1
            self.myLists_Layout.addWidget(Details(obj, self.data, self.dependencyPanel, self.refactor_rerender, self.dependencyPanel2, number, self.setFocusedIndex, index)) 
        
        # traceback.print_stack()

    def goFocus(self, index):
        QTimer.singleShot(0, lambda: self.myLists_Layout.itemAt(index).widget().setFocus())
        
    
    def setFocusedIndex(self, indexToGo) :
        numberToGo = (self.pageNav.currentPage - 1) * self.rows + indexToGo
        print(numberToGo, self.totalCount)
        if numberToGo > self.totalCount :
            self.focusedIndex = 1
        elif indexToGo == 0 :
            if self.pageNav.currentPage == 1 :
                # is first page
                self.focusedIndex = min(self.totalCount, self.rows)
            else :
                # is not first page
                self.pageNav.handleNavClicked('<')
                self.focusedIndex = self.rows
        elif indexToGo <= self.rows :
            self.focusedIndex = indexToGo
        else : # is beyond rows
            if self.pageNav.currentPage == self.pageNav.currentLastPage :
                # is last page
                self.focusedIndex = 1
            else:
                self.pageNav.handleNavClicked('>')
                self.focusedIndex = 1
        
        self.goFocus(self.focusedIndex)
    
    def refactor_rerender(self, Type = None, query_Params = None) :
        self.init_Query['fetchedList'] = self.getList()
  
        if (Type == 'filter') :
            self.init_Query['filter_Params'] = query_Params['filter']
        elif (Type == 'search') :
            self.init_Query['searchedBy'] = query_Params['searchBy']
            self.init_Query['keyword'] = query_Params['keyword']
        elif (Type == 'sort') :
            self.init_Query['sort'] = query_Params['sort']

        self.clear_layout(self.myLists_Layout)
        self.queriedArr = Query.refactor_Query(self.init_Query) 

        paginatedArr = getPage(self.queriedArr, self.pageNav.currentPage, self.rows)
        self.renderList(paginatedArr)
        self.pageNav.updateNav(self.queriedArr, self.rows)
        total = len(self.init_Query['fetchedList'])
        self.totalCount = total
        self.countLabel.setText(f"Total {self.data} : {total}")

    def getList(self): 
        with open(f"data/{self.data}.csv", 'r') as csvfile: 
            reader = csv.DictReader(csvfile)
            return list(reader)

    def clear_layout(self, layout):
        if layout is not None:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                widget = item.widget() 
                if widget: 
                    widget.deleteLater()
        # gc.collect()
        # print(gc.get_objects())
        # for i in range(self.myLists_Layout.count()):
        #     widget = self.myLists_Layout.itemAt(i).widget()
        #     print(f"Index {i}: {widget} ({type(widget)})")

    def resizeDynamically(self, height) :
        frame_inertHeight = 375 - 38
        detailFrame_height = 38
        self.rows = math.floor((height - frame_inertHeight) / detailFrame_height)
        self.refactor_rerender()


