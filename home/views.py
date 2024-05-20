from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from Account.models import Account
from home.models import Posting
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import DeepLake
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
import os
load_dotenv()
user=get_user_model()

openai_api_key = os.getenv('OPENAI_API_KEY')
def get_pdf_text():
    text = """Problem Statement:
Establish a platform that connects freelancers with potential clients, enhancing visibility and
opportunities.

Solution:

Title: Bridging the Gap: How Our Platform Connects Freelancers with Clients Seamlessly

In todays dynamic digital landscape, the demand for freelance services is booming. From graphic design
to content creation, businesses are increasingly turning to freelancers to meet their diverse needs.
However, with this surge in demand comes a new set of challenges for both freelancers and clients alike.
Finding the right match can be time-consuming and frustrating, often leading to missed opportunities and
underutilized talents.

Enter our innovative platform, designed to bridge the gap between freelancers and clients, revolutionizing
the way they connect and collaborate. Heres how it works:

* Comprehensive Profile Creation: Freelancers are invited to create detailed profiles showcasing their
skills, experience, and portfolio. Clients, on the other hand, can create profiles outlining their specific
project requirements and expectations.

* Advanced Search and Filtering: Our platform utilizes advanced search algorithms to match freelancers
with projects that align with their expertise and interests. Clients can easily filter through profiles based on
criteria such as skills, experience level, and budget.

* Real-time Communication: Once a potential match is identified, our platform facilitates seamless
communication between freelancers and clients through integrated messaging tools. This allows for
efficient collaboration and ensures that both parties are on the same page from the outset.

* Resource Center and Support: In addition to facilitating connections, our platform serves as a valuable
resource center for freelancers and clients alike. From best practices for project management to tips for
negotiating contracts, our platform offers comprehensive support every step of the way.

* Continuous Improvement: We are committed to continuously improving our platform based on user
feedback and industry trends. Through regular updates and enhancements, we strive to provide the best
possible experience for freelancers and clients alike.

In conclusion, our platform offers a user-friendly and efficient solution to the challenges of connecting
freelancers with clients. By leveraging cutting-edge technology and fostering a supportive community, we
empower freelancers to showcase their talents and help clients find the perfect match for their projects.
Join us and experience the future of freelance collaboration today!

 """
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    dataset_path = "./my_deeplake/"
    embeddings = OpenAIEmbeddings()
    vectorstore = DeepLake.from_texts(text_chunks,dataset_path=dataset_path, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore,user_question):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    memory = ConversationBufferMemory(memory_key='chat_history')
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=vectorstore.as_retriever(),
    )
    user_question += 'Draft the response in less than 50 words.'
    response = conversation_chain({'question':user_question})
    return response['answer']

def home(request):
    user_id = request.user.id
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass

    if request.method == 'POST':
        user_question = request.POST['chatinput']
        raw_text = get_pdf_text()
        text_chunks = get_text_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks)
        response = get_conversation_chain(vectorstore,user_question)
        context['content'] = response
        DeepLake.force_delete_by_path("./my_deeplake/")

    return render(request, 'home/home.html',context)

def job_posting(request):
    user_id = request.user.id
    customer = request.user.customer
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass

    if request.method == 'POST':
        Posting.objects.create(
            customer=customer,
            title=request.POST['title'],
            abstract=request.POST['abstract'],
            detail_description=request.POST['description'],
            skills=request.POST['skills'],
            budget=request.POST['budget'],
            image=request.FILES['image']
        )
        return redirect('home')
    return render(request, 'home/job_posting.html',context)

def list_jobs(request):
    user_id = request.user.id
    customer = request.user.customer
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass
    context['jobs'] = Posting.objects.filter(customer=customer)
    return render(request, 'home/list_jobs.html',context)

def list_all_jobs(request):
    user_id = request.user.id
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass

    if request.method == 'POST':
        context['jobs'] = Posting.objects.filter(title__contains=request.POST['search'])
    else:
        context['jobs'] = Posting.objects.all()
    return render(request, 'home/list_all_jobs.html',context)

def job_detail(request,job_id):
    user_id = request.user.id
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass
    context['job'] = Posting.objects.get(pk=job_id)
    return render(request, 'home/job_detail.html',context)

def ai_jobs(request):
    user_id = request.user.id
    context = {}
    try:
        account = Account.objects.get(pk=user_id)
        if account:
            context['profile_image'] = account.ImageURL
    except:
        pass

    return render(request, 'home/ai_jobs.html',context)
