var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
            matches.push(str);
        }
        });

        cb(matches);
    };
};

// $('#id_technologies_used').keyup(function(event){
//     console.log('ehllo')
//     if(event.keyCode == 13) {
//         event.preventDefault();
//     }
// });

// $('#id_technologies_used').tagsinput({
//     typeheadjs: {
//         name: 'states',
//         source: substringMatcher(states)
//     }
// });

var citynames = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
      url: 'assets/citynames.json',
      filter: function(list) {
        return $.map(list, function(cityname) {
          return { name: cityname }; });
      }
    }
  });
  citynames.initialize();
  
  $('#id_technologies_used').tagsinput({
    typeaheadjs: {
      name: 'citynames',
      displayKey: 'name',
      valueKey: 'name',
      source: citynames.ttAdapter()
    }
  });