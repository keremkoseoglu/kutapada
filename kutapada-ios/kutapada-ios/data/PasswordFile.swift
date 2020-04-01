//
//  PasswordFile.swift
//  kutapada-ios
//
//  Created by Dr. Kerem Koseoglu on 30.03.2020.
//  Copyright © 2020 Dr. Kerem Koseoglu. All rights reserved.
//

import Foundation

struct Header: Decodable {
    var format_version: String
    var encrypted: Bool
    
    init() {
        self.format_version = ""
        self.encrypted = false
    }
}

struct Account: Decodable, Hashable {
    var name: String
    var credential: String
    
    init() {
        self.name = ""
        self.credential = ""
    }
}

struct System: Decodable {
    var name: String
    var connection: String
    var accounts: [Account]
    
    init() {
        self.name = ""
        self.connection = ""
        self.accounts = [Account]()
    }
}

struct PasswordFile: Decodable {
    var header: Header
    var systems: [System]
    
    init() {
        self.header = Header()
        self.systems = [System]()
    }
}

extension String {

    var length: Int {
        return count
    }

    subscript (i: Int) -> String {
        return self[i ..< i + 1]
    }

    func substring(fromIndex: Int) -> String {
        return self[min(fromIndex, length) ..< length]
    }

    func substring(toIndex: Int) -> String {
        return self[0 ..< max(0, toIndex)]
    }

    subscript (r: Range<Int>) -> String {
        let range = Range(uncheckedBounds: (lower: max(0, min(length, r.lowerBound)),
                                            upper: min(length, max(0, r.upperBound))))
        let start = index(startIndex, offsetBy: range.lowerBound)
        let end = index(start, offsetBy: range.upperBound - range.lowerBound)
        return String(self[start ..< end])
    }
}

class PasswordJsonParser {
    
    private var passwordFile: PasswordFile?
    private var enc: [Character] = Array("1234567890qwertyuopasdfghjklizxcvbnm*-,.<é!'^+%&/()=?_';>:QWERTYUIOPASDFGHJKLZXCVBNM")
    private var dec: [Character] = Array("DH8G+.(YgJMx-6P:%)^sr>&<ob5f_wNKyiXRC7eIz!V4Z3EcjWnOa2?LmA/kpB'QlU=u;9*h0T'SFdqé1t,v")
    
    var flatAccountList: [Account] {
        get {
            var output = [Account]()
            for system in passwordFile!.systems {
                for account in system.accounts {
                    var flatAccount = Account()
                    flatAccount.name = system.name + " - " + account.name
                    flatAccount.credential = decodePassword(Encoded: account.credential)
                    output.append(flatAccount)
                }
            }
            return output
        }
    }
    
    func parseJson(JsonText: String) {
        self.passwordFile = try! JSONDecoder().decode(PasswordFile.self, from: JsonText.data(using: .utf8)!)
    }
    
    private func decodePassword(Encoded: String) -> String {
        if Encoded == "" { return "" }
        
        var new_credential = ""
        
        for e in Encoded {
            var idx = -1
            var found = -1
            for c in self.enc {
                idx += 1
                if c == e {
                    found = idx
                    break
                }
            }
            
            if found >= 0 {
                let decoded_char = self.dec[found]
                new_credential = new_credential + String(decoded_char)
            }
            else {
                new_credential = new_credential + String(e)
            }
            
        }
        
        return new_credential
    }
    
}
