from categories.models  import Category, BrandCategory

from Object.Get         import QuickObject

class GetContextForBrandCategoryList( object ):
    '''get the brand category list into the context'''
    
    def get_context_data(self, **kwargs):
        
        context = super(
            GetContextForBrandCategoryList, self
                ).get_context_data( **kwargs )
        #
        qsAllCategories = Category.objects.filter( iUser = self.request.user )
        #
        if self.object is None: # adding new brand
            #
            setBrandCategories = ()
            #
        else:
            #
            qsCategories = self.object.getCategoriesForBrand(self.object)
            #
            setBrandCategories = set( ( o.id for o in qsCategories ) )
            #
        #
        context['set_brand_categories'] = setBrandCategories
        #
        for oCategory in qsAllCategories:
            #
            oCategory.bIncluded = oCategory.id in setBrandCategories
            #
        #
        context['all_categories_list'] = qsAllCategories
        #
        if not hasattr( self, 'object' ) or self.object is None:
            # work around testing glitch
            self.object = QuickObject()
        if not hasattr( self.object, 'cTitle' ):
            # work around testing glitch
            self.object.cTitle = ''
        #
        lHelp = [
            '''<small>
            Checking the appropriate categories for %s is important
            <b>IF</b> you have any generic models -- model numbers/names
            that are shared by more than one brand.<br>'''
            % self.object.cTitle,
            '''If %s has model numbers/names that are shared by other brands,
            for the robot to be accurate, you <b>must</b> click on the
            categories below for the generic models.<br>'''
            % self.object.cTitle,
            '''(If %s does <b>not</b> have model numbers/names that are
            shared by other brands, never mind.)</small>'''
            % self.object.cTitle ]


        context['category_help'] = ''.join( lHelp )

        return context


class PostUpdateBrandCategoryList( object ):
    '''do post, handle the brand category updates'''

    def post(self, request, *args, **kwargs):
        '''handle changes to brand categories'''
        if "cancel" in request.POST:
            #
            pass
            #
        else: # 'submit' in request.POST
            #
            self.object = self.get_object()
            #
            setIncluded     = frozenset( request.POST.getlist('bIncluded'   ) )            
            setIncludedSet  = frozenset( request.POST.getlist('IncludedSet' ) )
            #
            setMustInclude  = setIncluded - setIncludedSet
            setMustUnInclude= setIncludedSet - setIncluded
            #
            self.object = self.get_object()
            #
            for sID in setMustInclude:
                #
                oBrandCategory = BrandCategory(
                        iBrand          = self.object,
                        iCategory_id    = int( sID ),
                        bWant           = True,
                        iUser           = self.request.user )
                #
                oBrandCategory.save()
                #
            #
            if setMustUnInclude:
                #
                qsDelete = BrandCategory.objects.filter( 
                        iBrand          = self.object,
                        iCategory_id__in= setMustUnInclude,
                        iUser           = self.request.user ).delete()
            #
        #
        return ( super( PostUpdateBrandCategoryList, self )
                    .post( request, *args, **kwargs ) )
