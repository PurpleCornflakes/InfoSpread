void Randomization_DegPre(Graph *p)//randomize real graph, degree preserving. AB,CD---AD,BC. rewire k*l times (100*E_num) 
{
	int i,j,x,k,l;//rewire k*l times (100*E_num)
	unsigned long int degree_accu[30000];
	unsigned long int edge_core;
	unsigned long int r1,r2;
	int node_i,node_j;
	int seq_edge1, seq_edge2;//to record the seq of edge for node i to be chosen
	E_type *current_i, *current_j;
	int count;
	int i_nb,j_nb;//the node of the other end, for node i and j
	int temp,temp_i,temp_j;
	bool flag=0;//this is to sign whether already exists cross edge
	E_type *current_f;
	FILE *fp_write;
	

	for (i=0;i<30000;i++)
		degree_accu[i]=0;
	
	j=0;//accumulated the degree for all nodes
	degree_accu[0]=0;//from array [1] to record the accumulated degree value
	for(i=1;i<p->V_num+1;i++)
	{
		if (j==0)
		{
			degree_accu[i]=p->vert[j].Degree;//for the first node, its degree is the accumulated value
			j++;
		}
		else
		{
			degree_accu[i]=p->vert[j].Degree+degree_accu[i-1];//for other nodes, add the degree with former accumulated degree
			j++;
		}
	}
	edge_core=degree_accu[p->V_num];//the total edge number. the edge number is from 1 to edge_core
	cout<<"edge"<<edge_core<<endl;
	cout<<"number of edge in the graph "<<p->E_num<<endl;

	//test, to output the accumulated degree for nodes
	/*for (i=1;i<p->V_num+1;i++)
		cout<<"accumulated degree of node "<<i-1<<" is "<<degree_accu[i]<<endl;
	cin>>x;*/
	

	for (k=0;k<100;k++)//rewire 100*E_num times
	{
		for(l=0;l<p->E_num;l++)
		{
			//cout<<"begin to generate r1 "<<endl;
			//cin>>x;
			r1=rand()*rand()%(edge_core+1);// the random number is from 0~edge_core
			while (r1==0)
				r1=rand()*rand()%(edge_core+1);
			//cout<<"r1 is "<<r1<<endl;
			//cin>>x;
			
			temp=p->V_num-1;//from the last node, find the node_i
			
			
			while (r1<=degree_accu[temp+1])
			{
				//cout<<"current test node i is "<<node_i<<" and its accumulated degree value is "<<degree_accu_core[temp+1]<<endl;
				temp=temp-1;
				//node_i=corenodes[temp];
				
			}
			seq_edge1=r1-degree_accu[temp+1];//the edge seq to be rewired is find
			node_i=temp+1;
			//cout<<"the node i is "<<node_i<<" and the seq of edge is "<<seq_edge1<<endl;
			//cin>>x;
			
			r2=rand()*rand()%(edge_core+1);// the random number is from 0~edge_core
			while (r2==0)
				r2=rand()*rand()%(edge_core+1);
			//cout<<"r2 is "<<r2<<endl;
			
			temp=p->V_num-1;//from the last node, find the node_j
			
			
			while (r2<=degree_accu[temp+1])
			{
				//cout<<"current test node i is "<<node_i<<" and its accumulated degree value is "<<degree_accu_core[temp+1]<<endl;
				temp=temp-1;
				
				
			}
			seq_edge2=r2-degree_accu[temp+1];//the edge seq to be rewired is find in the core
			node_j=temp+1;
			//cout<<"the node j is "<<node_j<<" and the seq of edge is "<<seq_edge2<<endl;
			//cin>>x;

			//now to find node i's neighbor and node j's neighbor
			current_i=p->vert[node_i].first->next;
			for (i=1;i<seq_edge1;i++)
				current_i=current_i->next;
			i_nb=current_i->Adjv_seq;
			
			current_j=p->vert[node_j].first->next;
			for (i=1;i<seq_edge2;i++)
				current_j=current_j->next;
			j_nb=current_j->Adjv_seq;
			
			//cout<<"i's nb is "<<i_nb<<" and j's nb is "<<j_nb<<endl;
			//cin>>x;

			//Before change the edge end, check if there is already 1-4 edge or 2-3 edge
			flag=0;
			current_i=p->vert[node_i].first->next;
			while (current_i!=NULL)
			{
				if (current_i->Adjv_seq==j_nb)
				{
					flag=1;
					break;
				}
				else
					current_i=current_i->next;
			}
			current_j=p->vert[node_j].first->next;
			while (current_j!=NULL)
			{
				if (current_j->Adjv_seq==i_nb)
				{
					flag=1;
					break;
				}
				current_j=current_j->next;
			}
			//cout<<"current flag for multiple connection is "<<flag<<endl;
			//cin>>x;

			//check if there generate self-connections
			if (node_i==j_nb||node_j==i_nb)
				flag=1;
			//cout<<"current flag for self-connection is "<<flag<<endl;
			

			if (flag==1)// if there may generate multiple connection or self connection, re-generate random r1 and r2. 
			{
				l=l-1;//re-do this turn of iterate
				//flag=0;
				//cout<<"as the flag is 1, we need to redo this turn and k is reset to "<<k<<endl;
				continue;
			}		
			

			//cout<<"now to change the edge end "<<endl;
			//now to change the edge end, after check 
			current_i=p->vert[node_i].first->next;//1->4
			for (i=1;i<seq_edge1;i++)
				current_i=current_i->next;
			current_i->Adjv_seq=j_nb;
			//cout<<"1-4 finished "<<endl;
					
			current_j=p->vert[node_j].first->next;//3->2
			for (j=1;j<seq_edge2;j++)
				current_j=current_j->next;
			current_j->Adjv_seq=i_nb;
			//cout<<"3-2 finished "<<endl;
			
			
			current_i=p->vert[i_nb].first->next;//2->3
			temp_i=current_i->Adjv_seq;
			while (temp_i!=node_i)
			{
				//cout<<"current temp_i is "<<temp_i<<endl;
				current_i=current_i->next;
				temp_i=current_i->Adjv_seq;
			}
			//cout<<"final find temp_i is "<<temp_i<<endl;
			current_i->Adjv_seq=node_j;
			//cout<<"2-3 finished "<<endl;
			//cin>>x;

			current_j=p->vert[j_nb].first->next;//4->1
			temp_j=current_j->Adjv_seq;
			while (temp_j!=node_j)
			{
				current_j=current_j->next;
				temp_j=current_j->Adjv_seq;
			}
			//cout<<"final find temp_j is "<<temp_j<<endl;
			current_j->Adjv_seq=node_i;
			//cout<<"4-1 finished "<<endl;
			
			//cout<<"rewire 1 pair finished "<<endl;
			//cin>>x;


		}
		cout<<"round "<<k<<" finished"<<endl;
		//cin>>x;
		
	}

	//now save the new graph
	
	if((fp_write = fopen("randomized_graph.txt","a")) == NULL) {
		printf("Cannot open file\n");
		exit(0);
	}
	for(i=0;i<p->V_num;i++)
	{
		current_f=p->vert[i].first->next;
		while (current_f!=NULL)
		{
			fprintf(fp_write,"%d  ",i); //cout<<i <<" ";
			fprintf(fp_write,"%d ", current_f->Adjv_seq); //cout<<current_f->Adjv_seq<<endl;
			fprintf(fp_write,"\n"); 
			current_f=current_f->next;
		}
		//if (i==5)
		//cout<<"node 4 in and out degree "<<p->vert[i].inDegree<<"  "<<p->vert[i].outDegree<<endl;		
	}
	fclose(fp_write);
}

void Randomization_DegCorPre(Graph *p)//randomize real graph, degree-degree correlation preserving. AB,CD---AD,BC. rewire k*l times (100*E_num) 
{
	int i,j,x,k,l;//rewire k*l times (100*E_num)
	unsigned long int degree_accu[30000];
	unsigned long int edge_core;
	unsigned long int r1,r2;
	int node_i,node_j;
	int seq_edge1, seq_edge2;//to record the seq of edge for node i to be chosen
	E_type *current_i, *current_j;
	int count;
	bool flag_samek=0;//flag to show if there exists at least two edges of the same degree.
	int i_nb,j_nb;//the node of the other end, for node i and j
	int temp,temp_i,temp_j;
	bool flag=0;//this is to sign whether already exists cross edge
	E_type *current_f;
	FILE *fp_write;
	

	for (i=0;i<30000;i++)
		degree_accu[i]=0;
	
	j=0;//accumulated the degree for all nodes
	degree_accu[0]=0;//from array [1] to record the accumulated degree value
	for(i=1;i<p->V_num+1;i++)
	{
		if (j==0)
		{
			degree_accu[i]=p->vert[j].Degree;//for the first node, its degree is the accumulated value
			j++;
		}
		else
		{
			degree_accu[i]=p->vert[j].Degree+degree_accu[i-1];//for other nodes, add the degree with former accumulated degree
			j++;
		}
	}
	edge_core=degree_accu[p->V_num];//the total edge number. the edge number is from 1 to edge_core
	cout<<"edge"<<edge_core<<endl;
	cout<<"number of edge in the graph "<<p->E_num<<endl;

	//test, to output the accumulated degree for nodes
	/*for (i=1;i<p->V_num+1;i++)
		cout<<"accumulated degree of node "<<i-1<<" is "<<degree_accu[i]<<endl;
	cin>>x;*/
	

	for (k=0;k<100;k++)//rewire 100*E_num times
	{
		for(l=0;l<p->E_num;l++)
		{
			//cout<<"begin to generate r1 "<<endl;
			//cin>>x;
			r1=rand()*rand()%(edge_core+1);// the random number is from 0~edge_core
			while (r1==0)
				r1=rand()*rand()%(edge_core+1);
			//cout<<"r1 is "<<r1<<endl;
			//cin>>x;
			
			temp=p->V_num-1;//from the last node, find the node_i
			
			
			while (r1<=degree_accu[temp+1])
			{
				//cout<<"current test node i is "<<node_i<<" and its accumulated degree value is "<<degree_accu_core[temp+1]<<endl;
				temp=temp-1;
				
				
			}
			seq_edge1=r1-degree_accu[temp+1];//the edge seq to be rewired is find in the core
			node_i=temp+1;
			//cout<<"node i is "<<node_i<<" and its degree is "<<p->vert[node_i].Degree<<endl;
			//cout<<"the node i is "<<node_i<<" and the seq of edge is "<<seq_edge1<<endl;
			//cin>>x;
			
			//to detect if there exists at least one edges that has the same degree node as node_i. If no, choose another edge for node i.
			flag_samek=0;
			for(i=0;i<p->V_num;i++)
			{
				if ((p->vert[i].Degree==p->vert[node_i].Degree)&&(node_i!=i))
				{
					flag_samek=1;
					break;
				}
			}

			if (flag_samek==0)
			{
				l=l-1;
				continue;
			}

						
			while (1)
			{
				r2=rand()*rand()%(edge_core+1);// the random number is from 0~edge_core
				while (r2==0||r2==r1)
					r2=rand()*rand()%(edge_core+1);
				//cout<<"r2 is "<<r2<<endl;
				
				temp=p->V_num-1;//from the last node, find the node_j
				//node_i=corenodes[temp];
				//cout<<"first core node "<<node_i<<" and its accumulated degree value is "<<degree_accu_core[temp+1]<<endl;
				
				while (r2<=degree_accu[temp+1])
				{
					//cout<<"current test node i is "<<node_i<<" and its accumulated degree value is "<<degree_accu_core[temp+1]<<endl;
					temp=temp-1;
					//node_i=corenodes[temp];
					
				}
				seq_edge2=r2-degree_accu[temp+1];//the edge seq to be rewired is find in the core
				node_j=temp+1;
				
				if ((p->vert[node_i].Degree==p->vert[node_j].Degree)&&(node_i!=node_j))
					break;												
			}
			//cout<<"node j is "<<node_j<<" and its degree is "<<p->vert[node_j].Degree<<endl;
			//cout<<"the node j is "<<node_j<<" and the seq of edge is "<<seq_edge2<<endl;
			//cin>>x;
			

			//now to find node i's neighbor and node j's neighbor
			current_i=p->vert[node_i].first->next;
			for (i=1;i<seq_edge1;i++)
				current_i=current_i->next;
			i_nb=current_i->Adjv_seq;
			
			current_j=p->vert[node_j].first->next;
			for (i=1;i<seq_edge2;i++)
				current_j=current_j->next;
			j_nb=current_j->Adjv_seq;
			
			//cout<<"i's nb is "<<i_nb<<" and j's nb is "<<j_nb<<endl;
			//cin>>x;

			//Before change the edge end, check if there is already 1-4 edge or 2-3 edge
			flag=0;
			current_i=p->vert[node_i].first->next;
			while (current_i!=NULL)
			{
				if (current_i->Adjv_seq==j_nb)
				{
					flag=1;
					break;
				}
				else
					current_i=current_i->next;
			}
			current_j=p->vert[node_j].first->next;
			while (current_j!=NULL)
			{
				if (current_j->Adjv_seq==i_nb)
				{
					flag=1;
					break;
				}
				current_j=current_j->next;
			}
			//cout<<"current flag for multiple connection is "<<flag<<endl;
			//cin>>x;

			//check if there generate self-connections
			if (node_i==j_nb||node_j==i_nb)
				flag=1;
			//cout<<"current flag for self-connection is "<<flag<<endl;
			

			if (flag==1)// if there may generate multiple connection or self connection, re-generate random r1 and r2. 
			{
				l=l-1;//re-do this turn of iterate
				//flag=0;
				//cout<<"as the flag is 1, we need to redo this turn and k is reset to "<<k<<endl;
				continue;
			}		
			

			//cout<<"now to change the edge end "<<endl;
			//now to change the edge end, after check 
			current_i=p->vert[node_i].first->next;//1->4
			for (i=1;i<seq_edge1;i++)
				current_i=current_i->next;
			current_i->Adjv_seq=j_nb;
			//cout<<"1-4 finished "<<endl;
					
			current_j=p->vert[node_j].first->next;//3->2
			for (j=1;j<seq_edge2;j++)
				current_j=current_j->next;
			current_j->Adjv_seq=i_nb;
			//cout<<"3-2 finished "<<endl;
			
			
			current_i=p->vert[i_nb].first->next;//2->3
			temp_i=current_i->Adjv_seq;
			while (temp_i!=node_i)
			{
				//cout<<"current temp_i is "<<temp_i<<endl;
				current_i=current_i->next;
				temp_i=current_i->Adjv_seq;
			}
			//cout<<"final find temp_i is "<<temp_i<<endl;
			current_i->Adjv_seq=node_j;
			//cout<<"2-3 finished "<<endl;
			//cin>>x;

			current_j=p->vert[j_nb].first->next;//4->1
			temp_j=current_j->Adjv_seq;
			while (temp_j!=node_j)
			{
				current_j=current_j->next;
				temp_j=current_j->Adjv_seq;
			}
			//cout<<"final find temp_j is "<<temp_j<<endl;
			current_j->Adjv_seq=node_i;
			//cout<<"4-1 finished "<<endl;
			
			//cout<<"rewire 1 pair finished "<<endl;
			//cin>>x;
			//cout<<"edge l "<<l <<" rewired "<<endl;
		}
		cout<<"round "<<k<<" finished"<<endl;
		//cin>>x;
		
	}

	//now save the new graph
	
	if((fp_write = fopen("randomized_graph.txt","a")) == NULL) {
		printf("Cannot open file\n");
		exit(0);
	}
	for(i=0;i<p->V_num;i++)
	{
		current_f=p->vert[i].first->next;
		while (current_f!=NULL)
		{
			fprintf(fp_write,"%d  ",i); //cout<<i <<" ";
			fprintf(fp_write,"%d ", current_f->Adjv_seq); //cout<<current_f->Adjv_seq<<endl;
			fprintf(fp_write,"\n"); 
			current_f=current_f->next;
		}
		//if (i==5)
		//cout<<"node 4 in and out degree "<<p->vert[i].inDegree<<"  "<<p->vert[i].outDegree<<endl;		
	}
	fclose(fp_write);

}