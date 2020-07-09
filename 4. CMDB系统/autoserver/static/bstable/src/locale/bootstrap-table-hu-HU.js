/**
 * Bootstrap Table Hungarian translation
 * Author: Nagy Gergely <info@nagygergely.eu>
 */
($ => {
  $.fn.bootstrapTable.locales['hu-HU'] = {
    formatLoadingMessage () {
      return 'Betöltés, kérem várjon...'
    },
    formatRecordsPerPage (pageNumber) {
      return `${pageNumber} rekord per oldal`
    },
    formatShowingRows (pageFrom, pageTo, totalRows) {
      return `Megjelenítve ${pageFrom} - ${pageTo} / ${totalRows} összesen`
    },
    formatSearch () {
      return 'Keresés'
    },
    formatNoMatches () {
      return 'Nincs találat'
    },
    formatPaginationSwitch () {
      return 'Lapozó elrejtése/megjelenítése'
    },
    formatRefresh () {
      return 'Frissítés'
    },
    formatToggle () {
      return 'Összecsuk/Kinyit'
    },
    formatColumns () {
      return 'Oszlopok'
    },
    formatAllRows () {
      return 'Összes'
    }
  }

  $.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales['hu-HU'])
})(jQuery)
