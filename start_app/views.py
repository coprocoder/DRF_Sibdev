from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

# ---------------------------------------------------------------------------
from rest_framework import status
from rest_framework.views import APIView
from .models import File, Deal
from .serializers import FileSerializer

class FileUploadView(APIView):
    # parser_classes = (FileUploadParser)

    def get(self, request):

        # Show list files
        # files = File.objects.all()
        # serializer = FileSerializer(files, many=True)
        # return Response({"files": serializer.data})

        '''
            В данной работе несколько раз QuerySet преобразуется в List для комфортной работы в рамках задания.
            Согласно документации такой приём не желателен, но так как это моё первое знакомство с Django,
            и время выполнения ограничено, я предпочёл этот костыль в пользу скорости выполнения задания.

            В дальнейшем изучу больше методов Django ORM и постараюсь прибегать к паттернам
            вместо собственных обходных конструкций.
        '''

        from django.db.models import Sum

        # Get list of customers
        customers_names = list(set(Deal.objects.values_list('customer', flat=True)[0:50]))

        # Create list of dicts where dict = customer info
        customers = []
        for i in customers_names:
            customer_info = {
                'username': str(i),
                'spent_money': Deal.objects.filter(customer=str(i)).aggregate(Sum('total')).get("total__sum"),
                # Now it's list of all purchased gems
                'gems': Deal.objects.filter(customer=str(i)).values_list('item', flat=True).distinct()
            }
            customers.append(customer_info)
        customers.sort(key=lambda dictionary: dictionary['spent_money'], reverse = True)

        # Choice of customers who spent the most money
        top_customers = customers[:5]

        # List of all gems top_customers
        gems = []
        for customer in top_customers:
            customer_gems = list(customer.get("gems"))
            for gem in customer_gems:
                gems.append(gem)

        # Delete gems in customer_gems which occur less than twice
        for customer in top_customers:
            customer_gems = list(customer.get("gems"))
            customer_gems_copy = customer_gems.copy()
            for gem in customer_gems_copy:
                if(gems.count(gem)<2):
                    customer_gems.remove(gem)
            customer.update({'gems': customer_gems})

        return Response({"Response": top_customers})

    def post(self, request):
        up_file = request.FILES['file']
        up_file_path_to_save = 'media/' + up_file.name
        destination = open(up_file_path_to_save, 'wb+')
        for chunk in up_file.chunks():
            # print("=== File = " + str(chunk) + "\n\n")
            destination.write(chunk)
        destination.close()  # File should be closed only after all chuns are added

        # ------ do some stuff with uploaded file ------ #
        import csv
        with open(up_file_path_to_save, encoding="utf8") as deals_file:
            deals_data = csv.reader(deals_file, delimiter=',')
            for row in deals_data:
                if(row[0] != "customer" and row[4] != "date"): # to skip headers
                    deal = Deal.objects.create(
                        customer = row[0],
                        item = row[1],
                        total=row[2],
                        quantity=row[3],
                        date=row[4]
                    )
            print("CSV data imported in DB")

                    # deal = Deal()
                    # deal.customer = row[0]
                    # deal.item = row[1]
                    # deal.total = row[2]
                    # deal.quantity = row[3]
                    # deal.date = row[4]
                    # deal.save()

        return Response(up_file.name, status.HTTP_201_CREATED)

    def put(self, request, pk):
        saved_file = get_object_or_404(File.objects.all(), pk=pk)
        data = request.data.get('datafile')
        serializer = FileSerializer(instance=saved_file, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            file_saved = serializer.save()
        return Response({
            "success": "File '{}' updated successfully".format(file_saved.datafile)
        })

    def delete(self, request, pk):
        # Get object with this pk
        file = get_object_or_404(File.objects.all(), pk=pk)
        file.delete()
        return Response({
            "message": "File with id `{}` has been deleted.".format(pk)
        }, status=204)

# ---------------------------------------------------------------------------
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer

# For additional modules (не по ТЗ)
class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        article = request.data.get("article")
        # Create an article from the above data
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({
            "success": "Article '{}' updated successfully".format(article_saved.title)
        })

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)
