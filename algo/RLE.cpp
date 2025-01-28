#include <bits/stdc++.h>
using namespace std;

int main(){
    string s;
    cin >> s;
    int n = s.size();
    int j = 0;
    // RLE
    for(int i = 0; i < n;){
        int cnt = 0;
        while(j < n && s[i] == s[j]){
            j++;
            cnt++;
        }
        cout << s[i] << cnt;
        i = j;
    }
}