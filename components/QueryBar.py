from PyQt6.QtWidgets import (
    QLineEdit,
    QWidget,
    QPushButton, 
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QFrame,
    )
from algo import getOptions
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QCursor

class QueryBar(QWidget) :
    def __init__(self, myList, data):
        super().__init__()
        self.myList = myList
        self.data = data

        self.defaultQuery = {
            "filter" : "no filter",
            "searchBy" : "everywhere",
            "keyword" : "",
            "sort" : "recent"
        }
        frame_layout = QHBoxLayout()

        if (self.data == 'students') :
            self.searchByLabel = QLabel('search by:')
            self.searchByComboBox = QComboBox()
            self.searchByComboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.searchByComboBox.addItems(['everywhere','id_no', 'first_name', 'last_name'])

        self.searchBar = QLineEdit()
        self.searchBar.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.searchBar.returnPressed.connect(self.refactor_handleSearch)
        self.searchBtn = QPushButton()
        self.searchBtn.setIcon(QIcon("searchIcon.svg"))
        self.searchBtn.setIconSize(QSize(24, 24))
        self.searchBtn.setStyleSheet("border:none; background-color: transparent;")
        self.searchBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.searchBtn.clicked.connect(self.refactor_handleSearch)

        self.sortComboBox = QComboBox()
        self.sortComboBox.currentIndexChanged.connect(self.refactor_handleSort)
        self.sortComboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if (self.data != 'colleges') :
            self.filterLabel = QLabel('Filter: ')
            self.filterComboBox = QComboBox()
            self.filterComboBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            self.filterComboBox.currentIndexChanged.connect(self.refactor_handleFilter)    

        if (self.data == 'students') :
            self.sortComboBox.blockSignals(True)
            self.sortComboBox.addItems(["recent", "oldest", "id no.↑", "id no.↓", "last name↑", "last name↓","year level↑", "year level↓"  ])
            self.sortComboBox.blockSignals(False)

            #filterBox
            self.filterComboBox.blockSignals(True)

            self.filterComboBox.addItem('no filter')
            self.filterComboBox.addItem("-- by College --")
            college_labelIndex = self.filterComboBox.count() -1
            self.filterComboBox.setItemData(college_labelIndex, False, Qt.ItemDataRole.UserRole -1)
            self.filterComboBox.addItems(getOptions.getColleges())
            self.filterComboBox.addItem("-- by Program --") 
            program_labelIndex = self.filterComboBox.count() - 1
            self.filterComboBox.setItemData(program_labelIndex, False, Qt.ItemDataRole.UserRole -1)
            self.filterComboBox.addItem('none')
            self.filterComboBox.addItems(getOptions.getPrograms())
            self.filterComboBox.blockSignals(False)

        elif (self.data == 'programs') :
            self.sortComboBox.blockSignals(True)
            self.sortComboBox.addItems(["recent", "oldest","a-z", "z-a", "college" ])
            self.sortComboBox.blockSignals(False)

            self.filterComboBox.blockSignals(True)
            self.filterComboBox.addItem('no filter')
            self.filterComboBox.addItem("-- by College --")
            college_labelIndex = self.filterComboBox.count() -1
            self.filterComboBox.setItemData(college_labelIndex, False, Qt.ItemDataRole.UserRole -1)
            self.filterComboBox.addItem('none')
            self.filterComboBox.addItems(getOptions.getColleges())
            self.filterComboBox.blockSignals(False)

        elif (self.data == 'colleges') :
            self.sortComboBox.blockSignals(True)
            self.sortComboBox.addItems(["recent", "oldest","a-z", "z-a" ])
            self.sortComboBox.blockSignals(False)

        if (self.data == 'students') : # students only has searchby
            frame_layout.addWidget(self.searchByLabel)
            frame_layout.addWidget(self.searchByComboBox)

        frame_layout.addWidget(self.searchBar)
        frame_layout.addWidget(self.searchBtn)
        frame_layout.addWidget(self.sortComboBox)
        if (self.data != 'colleges') : # college doesn't have filter
            frame_layout.addWidget(self.filterLabel)
            frame_layout.addWidget(self.filterComboBox)


        frame = QFrame()
        frame.setFixedHeight(70)
        frame.setLayout(frame_layout)
        
        if self.data == "students" :
            frame.setObjectName("studentQueryBar")
        elif self.data == "programs" :
            frame.setObjectName("programQueryBar")
        elif self.data == "colleges" :
            frame.setObjectName("collegeQueryBar")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
        main_layout.addWidget(frame)
        self.setLayout(main_layout)

    def refactor_handleFilter(self) :
        filterBy = self.filterComboBox.currentText()
        index = self.filterComboBox.findText(filterBy)
        program_index = self.filterComboBox.findText("-- by Program --")
        if filterBy == 'no filter' :
            filter_Params = {
                'filterBy':'no filter'
                }
        else :
            filter_Params = {
                'filterBy' : filterBy,
                'index' : index,
                'programLabel_index' : program_index,
                'data' : self.data,
            }
        self.defaultQuery['filter'] = filter_Params
    
        self.myList.refactor_rerender('filter', self.defaultQuery)

    def refactor_handleSearch(self) :
        keyword = self.searchBar.text() 

        self.defaultQuery['keyword'] = keyword

        if (self.data == 'students') :
            searchBy = self.searchByComboBox.currentText()
            self.defaultQuery['searchBy'] = searchBy

        self.myList.refactor_rerender('search', self.defaultQuery)

    def refactor_handleSort(self) :
        sortBy = self.sortComboBox.currentText()
        self.defaultQuery['sort'] = sortBy

        self.myList.refactor_rerender('sort', self.defaultQuery)

