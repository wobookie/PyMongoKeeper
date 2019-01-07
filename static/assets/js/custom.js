// Get references to page elements
const loader = document.getElementById("loaderId");
const filterInput = document.getElementById("inputFilterQuery");
const btnInput = document.getElementById("btnFilterSubmit");
const badgeInput = document.getElementById("badgeFilterInput");
const resultTable = document.getElementById("tableFilterResults");
const totalResultCountText = document.getElementById("totalRecordsID");
const textRecordRange = document.getElementById("recordRangeID");
const spanRecordRangeText = document.getElementById("spanRecordRangeText");
const ulPagination = document.getElementById("ulPagination");
const btnPaginationPrevious = document.getElementById("btnPaginationPrevious");
const btnPaginationNext = document.getElementById("btnPaginationNext");
const liPaginationPrevious = document.getElementById("liPaginationPrevious");
const liPaginationNext = document.getElementById("liPaginationNext");

var filterQuery = '{}';
var previousPagesOID = ['#'];

$("#btnPaginationNext").on("click", function (ev) {
    var oid = '#';
    var url = '/datafilter_next';

    if (!liPaginationNext.classList.contains("disabled")) {
        // do something
        console.log('Request next data set');

        try {
            oid = this.attributes['href'].nodeValue;
            console.log('for OID:' + oid);

            getDocuments(url, oid, filterQuery);

        } catch (err) {
            console.log(err);
        }

    }
});

$("#btnPaginationPrevious").on("click", function (ev) {
    var oid = '#';
    var url = '/datafilter_previous';

    if (!liPaginationPrevious.classList.contains("disabled")) {
        // do something
        console.log('Request previous data set');

        try {
            oid = this.attributes['href'].nodeValue;
            console.log('for OID:' + oid);

            getDocuments(url, oid, filterQuery);

        } catch (err) {
            console.log(err);
        }

    }
});

$("#btnFilterSubmit").on("click", function (ev) {
    var oid = '#';
    var url = '/datafilter';

    filterQuery = filterInput.value;

    if (!btnInput.classList.contains("disabled")) {
        getDocuments(url, oid, filterQuery);
    }
});

$("#inputFilterQuery").on("input", function () {

    if (IsValidJSONString($(this).val())) {
        btnInput.classList.remove("disabled");
        badgeInput.classList.remove("badge-danger");
        badgeInput.classList.add("badge-secondary");
    } else {
        btnInput.classList.add("disabled");
        badgeInput.classList.remove("badge-secondary");
        badgeInput.classList.add("badge-danger");
    }

});


function getDocuments(url, oid, filter) {
    $(resultTable).empty();
    spanRecordRangeText.classList.add("hidden");
    ulPagination.classList.add("hidden");

    $.ajax({
        url: url,
        data: {'oid': oid, 'filter': filter},
        type: 'POST',
        success: function (data) {
            renderDataTable(data)
        },
        error: function (error) {
            console.log('Ajax Error');
            console.log(error);

            loader.classList.remove("is-active");
        }
    });
}

function renderDataTable(data) {
    let documentsArray = data.doc_data;
    let totalDocCount = data.total_doc_count;
    let pageNumber = data.page_number;
    let pageSize = data.page_size;

    let startRowNumber = pageNumber * pageSize + 1;
    let endRowNumber = pageNumber * 10 + pageSize;

    if(endRowNumber >= totalDocCount) {
        endRowNumber = totalDocCount;
        liPaginationNext.classList.add("disabled");
    } else {
        liPaginationNext.classList.remove("disabled");
    }

    if(startRowNumber == 1) {
        liPaginationPrevious.classList.add("disabled");
    } else {
        liPaginationPrevious.classList.remove("disabled");
    }

    let recordRangeText = '' + startRowNumber + ' - ' + endRowNumber;

    try {
        let lastDocumentOID = JSON.parse(documentsArray[(documentsArray.length - 1)])['_id']['$oid'];

        if ((previousPagesOID.length - 1) == pageNumber) {
                previousPagesOID.push('#' + lastDocumentOID);
        }

        btnPaginationPrevious.setAttribute('href', previousPagesOID[0]);

        if (pageNumber > 0) {
            btnPaginationPrevious.setAttribute('href', previousPagesOID[pageNumber-1]);
        }

        btnPaginationNext.setAttribute('href', '#' + lastDocumentOID);

        $(resultTable).append($("<tbody/>"));

        $.each(documentsArray, function () {
            var row = $("<tr/>");
            row.append($("<td/>").text(this));
            $(resultTable).append(row);
        });

        $(textRecordRange).text(recordRangeText);
        $(totalResultCountText).text(totalDocCount);

        spanRecordRangeText.classList.remove("hidden");
        ulPagination.classList.remove("hidden");
    } catch(err) {
        console.log(err)
    } finally {
        loader.classList.remove("is-active");
    }
}

function IsValidJSONString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}

$(document).ready(function() {
});