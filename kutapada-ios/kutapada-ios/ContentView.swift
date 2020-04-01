//
//  ContentView.swift
//  kutapada-ios
//
//  Created by Dr. Kerem Koseoglu on 29.03.2020.
//  Copyright © 2020 Dr. Kerem Koseoglu. All rights reserved.
//

import SwiftUI

private let dateFormatter: DateFormatter = {
    let dateFormatter = DateFormatter()
    dateFormatter.dateStyle = .medium
    dateFormatter.timeStyle = .medium
    return dateFormatter
}()

struct ContentView: View {
    @State private var accounts = [Account]()
    
    var body: some View {
        NavigationView {
            MasterView(accounts: $accounts)
                .navigationBarTitle(Text("Accounts"))
                .navigationBarItems(
                    leading: NavigationLink(destination: DropboxAuthView()) {
                        Image(systemName: "cube.box")
                    },
                    

                    trailing: Button(
                        action: {
                            withAnimation { self.refreshList() }
                        }
                    ) {
                        Image(systemName: "arrow.clockwise.circle")
                    }
                )
            DetailView()
        }.navigationViewStyle(DoubleColumnNavigationViewStyle())
    }
    
    func refreshList() {
        let dropbox = DropBox()
        dropbox.readPasswordFileContent()
        sleep(4)
        let parser = PasswordJsonParser()
        if dropbox.passwordFileContent == "" {return}
        parser.parseJson(JsonText: dropbox.passwordFileContent)
        self.accounts = parser.flatAccountList
    }
}

struct MasterView: View {
    @Binding var accounts: [Account]

    var body: some View {
        List {
            ForEach(accounts, id: \.self) { account in
                NavigationLink(
                    destination: DetailView(selectedAccount: account)
                ) {
                    Text(account.name)
                }
            }.onDelete { indices in
                indices.forEach { self.accounts.remove(at: $0) }
            }
        }
    }
}

struct DetailView: View {
    var selectedAccount: Account?

    var body: some View {
        Group {
            if selectedAccount != nil {
                Text(selectedAccount!.credential)
            } else {
                Text("Detail view content goes here")
            }
        }.navigationBarTitle(Text("Detail"))
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct DropboxAuthView: View {
    @State var token: String = ""
    @State var dropbox: DropBox = DropBox()
    
    var body: some View {
        VStack(alignment: .center, spacing: 20) {
            Text("Finish authorization and enter token")
            Button(action: {withAnimation { self.dropbox.authorize() }}) {
                Text("Authorize")
            }
            TextField("Your DropBox token", text: $token)
            HStack(alignment: .center, spacing: 20) {
                Button(action: {withAnimation {
                    self.dropbox.token = self.token }})
                { Text("Save") }
            }
        }.navigationBarTitle(Text("Connect to DropBox"))
    }
    
}
