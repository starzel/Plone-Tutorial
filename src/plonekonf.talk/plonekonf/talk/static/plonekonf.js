(function($){
    if(window.plonekonf === undefined){
        window.plonekonf = {};
    }
    plonekonf.init_voting_viewlet = function(context){
        var notyetvoted = context.find("#notyetvoted");
        var alreadyvoted = context.find("#alreadyvoted");
        if(context.find("#voted").length !== 0){
            alreadyvoted.show();
        }else{
            notyetvoted.show();    
        }
            
        function vote(rating){
            return function inner_vote(){
                $.post(context.find("#context_url").attr('href') + '/vote',
                       {rating: rating},
                       function(){
                           location.reload();
                       });
            };
        };
        context.find("#voting_plus").click(vote(1));
        context.find("#voting_neutral").click(vote(0));
        context.find("#voting_negative").click(vote(-1));

        var delete_votings = context.find("#delete_votings");
        var delete_votings2 = context.find("#delete_votings2");
        delete_votings.click(function(){
            delete_votings2.toggle();
        });
        delete_votings2.click(function(){
            $.post(context.find("#context_url").attr("href") + "/clearvotes",
                   function(){
                       location.reload();
                   });
        });
    };
})(jQuery);
